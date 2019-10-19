import asyncio
import json
import logging
from dataclasses import asdict
from typing import *

from pyee import BaseEventEmitter
from rx.subject import Subject

from desktop.lib.api import API
from desktop.lib.auth import get_key_for_account
from desktop.lib.common import with_logger
from desktop.lib.json import json_generator
from desktop.lib.models.account import Account, fetch_user
from desktop.lib.stores.stores import IKeyValueStore, ISecureStore
from aiosqlite import Connection, Cursor


@with_logger
class AccountsStore:
    def __init__(self, key_value_store: IKeyValueStore,
                 secure_store: ISecureStore,
                 error_subject: Subject,
                 accounts_updated_subject: Subject,
                 provide_api: Callable[[str, str], API]):
        super().__init__()
        self.data_store = key_value_store
        self.security_store = secure_store
        self.provide_api = provide_api
        self.emitter = BaseEventEmitter()
        self.accounts_updated_subject = accounts_updated_subject
        self.error_subject = error_subject
        self.loading_task = asyncio.create_task(self.__load_from_store())
        self.accounts = []

    async def get_all(self) -> List[Account]:
        await self.loading_task
        return self.accounts.copy()

    async def add_account(self, account: Account) -> Optional[Account]:
        await self.loading_task

        try:
            updated = await self.updated_account(account)
        except Exception as e:
            self._logger.warning(f"Failed to fetch user {account.login}", e)
            raise

        try:
            await self.security_store.set_item(
                get_key_for_account(updated),
                updated.login,
                updated.token
            )
        except Exception as e:
            self._logger.error(f"Error adding account '{account.login}'", e)
            self.error_subject.on_next(e)
            return None

        self.accounts.append(updated)
        self.accounts_updated_subject.on_next(list(self.accounts))
        await self.save()
        return updated

    async def refresh(self):
        futures = map(lambda acc: self.__try_update_account(acc), self._accounts)
        result, _ = await asyncio.wait(futures)
        self.accounts = [f.result for f in result]
        self.accounts_updated_subject.on_next(list(self.accounts))
        await self.save()

    async def remove_account(self, account: Account):
        await self._loading_task
        try:
            await self._security_store.delete_item(get_key_for_account(account),
                                                   account.login)
        except Exception as e:
            self.logger.error(f"Error removing account '{account.login}'", e)
            self.error_subject.on_next(e)
            return
        else:
            self.accounts = filter(lambda a: a.id != account.id, self._accounts)
            await self.save()

    async def save(self):
        users_without_tokens = [account.with_token('') for account in self.accounts]
        result = json_generator(users_without_tokens)
        await self.data_store.set_item('users', result)

    async def __try_update_account(self, acc: Account):
        try:
            return await self.updated_account(acc)
        except Exception as e:
            self.logger.warn(f"Error refreshing account '{acc.login}'", e)
            return acc

    async def __load_from_store(self):
        raw = await self.data_store.get_item('users')
        if not raw:
            return

        raw = json.loads(raw)
        accounts_with_tokens = []
        for item in map(lambda i: Account.from_dict(i), raw):
            account_without_token = Account(**(asdict(item)))
            key = get_key_for_account(account_without_token)
            try:
                token = await self.security_store.get_item(key, item.login)
                accounts_with_tokens.append(account_without_token.with_token(token))
            except Exception as e:
                logging.error(f"Error getting token for '{key}'. Skipping.", e)
                self.emit_error(e)
        self.accounts = accounts_with_tokens
        self.accounts_updated_subject.on_next(self.accounts)

    async def updated_account(self, account: Account) -> Account:
        if not account.token:
            raise Exception(f"Cannot update an account which doesn't have a token: {account.login}")
        return await fetch_user(self.provide_api(account.endpoint, account.token))
