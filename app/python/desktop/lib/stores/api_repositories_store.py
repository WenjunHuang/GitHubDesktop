from dataclasses import dataclass, replace
from typing import List, Mapping, Optional, Tuple

from desktop.lib.api import APIRepositoryData, API
from desktop.lib.models.account import Account
from desktop.lib.stores.accounts_store import AccountsStore
from desktop.lib.stores.base_store import BaseStore


@dataclass
class AccountRepositories:
    repositories: List[APIRepositoryData]


class ApiRepositoriesStore(BaseStore):
    _account_state: Mapping[Account, AccountRepositories]

    def __init__(self, accounts_store: AccountsStore):
        super().__init__()
        self._account_state = {}
        accounts_store.update.connect(self.__on_accounts_changed)

    async def load_repositories(self, account: Account) -> AccountRepositories:
        existing_account = resolve_account(account, self._account_state)
        existing_repositories = self._account_state.get(existing_account)

        if existing_repositories and existing_repositories.loading:
            return

        self.__update_account(existing_account, loading=True)
        api = API(existing_account.endpoint, existing_account.token)
        repositories = await api.fetch_repositories()

        if not repositories:
            self.__update_account(account, loading=False)
        else:
            self.__update_account(account, loading=False, repositories=repositories)

    def get_state(self):
        return self._account_state

    def __update_account(self, account: Account, *, loading: Optional[bool] = None,
                         repositories: Optional[List[APIRepositoryData]] = None):
        new_state = dict(self._account_state)
        newOrExistingAccount = resolve_account(account, new_state)
        existing_repositories = new_state.get(newOrExistingAccount, AccountRepositories(loading=False,
                                                                                        repositories=[]))

        update = {}
        if loading:
            update['loading'] = loading
        if repositories:
            update['repositories'] = repositories
        new_repositories = replace(existing_repositories, **update)
        new_state[newOrExistingAccount] = new_repositories
        self._account_state = new_state
        self.emit_update(self._account_state)

    def __on_accounts_changed(self, accounts: List[Account]):
        new_state = {}
        for account in accounts:
            for key, value in self._account_state.items():
                if account_equals(key, account):
                    new_state[account] = value
                    break

        self._account_state = new_state
        self.emit_update(self._account_state)


def account_equals(x: Account, y: Account) -> bool:
    return x.endpoint == y.endpoint and x.id == y.id


def resolve_account(account: Account,
                    account_state: Mapping[Account, AccountRepositories]):
    if account in account_state:
        return account

    for existing_account in account_state.keys():
        if account_equals(existing_account, account):
            return existing_account
    return account
