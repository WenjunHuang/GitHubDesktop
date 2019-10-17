import os
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

    def __init__(self):
        super().__init__()

    async def load_initial_state(self):
        config_dir = await get_config_dir()
        await self.initialize_database(config_dir)
        self.init_key_value_store()
        self.init_key_value_store()

        self.github_user_database = GitHubUserDatabase(self.database)
        self.account_store = AccountsStore(self.key_value_store, self.secure_store)

    async def initialize_database(self, config_dir: str):
        db_file = 'desktop.db'
        db_file_path = os.path.join(config_dir, db_file)
        db = await aiosqlite.connect(db_file_path)

        def namedtuple_factory(cursor, row):
            fields = [col[0] for col in cursor.description]
            Row = namedtuple('Row', fields)
            return Row(*row)

        db.row_factory = namedtuple_factory()

        self.database = db

    def init_key_value_store(self):
        key_value_store = KeyValueStore(self.database)
        self.key_value_store = key_value_store

    def init_secure_store(self):
        self.secure_store = TokenStore()


async def get_config_dir():
    # 获取配置存储的目录
    return os.getcwd()


app_store = AppStore()


def get_app_store():
    return app_store
