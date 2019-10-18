import asyncio
import os
import sqlite3
from collections import namedtuple

import aiosqlite
from PyQt5.QtCore import QObject
from aiosqlite import Connection

from desktop.lib.databases.github_user_database import GitHubUserDatabase
from desktop.lib.stores import IKeyValueStore, AccountsStore
from desktop.lib.stores.key_value_store import KeyValueStore
from desktop.lib.stores.token_store import TokenStore


class AppStore(QObject):
    database: Connection
    github_user_database: GitHubUserDatabase
    key_value_store: IKeyValueStore
    account_store: AccountsStore

    def __init__(self, config_dir: str):
        super().__init__()
        self._config_dir = config_dir

    async def load_initial_state(self):
        config_dir = self._config_dir
        await self.initialize_database(config_dir)
        self.init_key_value_store()
        self.init_secure_store()

        self.github_user_database = GitHubUserDatabase(self.database)
        self.account_store = AccountsStore(self.key_value_store, self.secure_store)

    async def initialize_database(self, config_dir: str):
        db_file = 'desktop.db'
        db_file_path = os.path.join(config_dir, db_file)
        db = await aiosqlite.connect(db_file_path)

        db.row_factory = sqlite3.Row
        self.database = db

    def init_key_value_store(self):
        key_value_store = KeyValueStore(self.database)
        self.key_value_store = key_value_store

    def init_secure_store(self):
        self.secure_store = TokenStore()


app_store: AppStore = None


def init_app_store(config_dir: str):
    global app_store
    app_store = AppStore(config_dir)
    asyncio.get_event_loop().run_until_complete(app_store.load_initial_state())


def get_app_store():
    return app_store
