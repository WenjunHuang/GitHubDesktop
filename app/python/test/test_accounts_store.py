import asyncio
import unittest
from collections import namedtuple

import aiosqlite
import sqlite3

from desktop.lib.api import get_dotcom_api_endpoint
from desktop.lib.http import init_session, get_session
from desktop.lib.stores import AccountsStore, Account
from desktop.lib.stores.key_value_store import KeyValueStore
from desktop.lib.stores.token_store import TokenStore


class TestAccountsStore(unittest.TestCase):
    def setUp(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.database = self.loop.run_until_complete(aiosqlite.connect("./test_db"))

        self.database.row_factory = sqlite3.Row
        self.key_value_store = KeyValueStore(self.database)
        self.secure_store = TokenStore()
        init_session()

    def tearDown(self) -> None:
        self.loop.run_until_complete(get_session().close())
        self.loop.stop()

    def test_get_all(self):
        async def run():
            test = AccountsStore(self.key_value_store, self.secure_store)
            return await test.get_all()

        self.loop.run_until_complete(run())

    def test_add_account(self):
        async def run():
            test = AccountsStore(self.key_value_store, self.secure_store)
            test_account = Account(login='WenjunHuang',
                                   endpoint=get_dotcom_api_endpoint(),
                                   token='0158b5b23f25d95a03766377fcc300bd3025ce6e', emails=[],
                                   avatar_url='http://avatar.com',
                                   id=1,
                                   name='demo')
            return await test.add_account(test_account)

        self.loop.run_until_complete(run())
