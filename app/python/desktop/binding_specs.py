import asyncio
import os
import sqlite3
import sys

import aiohttp
import aiosqlite
import pinject
import rx
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from aiosqlite import Connection
from asyncqt import QEventLoop

from desktop.lib.api import API
from desktop.lib.databases.github_user_database import GitHubUserDatabase
from desktop.lib.json import json_generator
from desktop.lib.stores.key_value_store import KeyValueStore
from desktop.lib.stores.token_store import TokenStore


class BasicBindingSpec(pinject.BindingSpec):
    def provide_app(self):
        sys_args = sys.argv
        sys_args += ['--style', './ui/common']
        return QGuiApplication(sys_args)

    def provide_qml_engine(self, app):
        # must dependent on app
        return QQmlApplicationEngine()

    def provide_event_loop(self, app):
        loop = QEventLoop(app)
        asyncio.set_event_loop(loop)
        asyncio.events._set_running_loop(loop)
        return loop


class DatabaseBindingSpec(pinject.BindingSpec):
    def provide_database(self, config_dir):
        db_file = 'desktop.db'
        db_file_path = os.path.join(config_dir, db_file)
        db = asyncio.get_event_loop().run_until_complete(aiosqlite.connect(db_file_path))
        db.row_factory = sqlite3.Row
        return db

    def provide_github_user_database(self, database):
        return GitHubUserDatabase(database)


class HttpApiBindingSpec(pinject.BindingSpec):
    @pinject.provides(in_scope=pinject.PROTOTYPE)
    @pinject.inject(['http_session'])
    def provide_api(self, endpoint, token, http_session):
        return API(endpoint, token, http_session)

    def provide_http_session(self):
        # return event_loop.run_until_complete(aiohttp.ClientSession(json_serialize=json_generator))
        return aiohttp.ClientSession(json_serialize=json_generator)

    def dependencies(self):
        return [BasicBindingSpec()]


class StoreBindingSpec(pinject.BindingSpec):
    def provide_key_value_store(self, database: Connection):
        key_value_store = KeyValueStore(database)
        return key_value_store

    def provide_secure_store(self):
        secure_store = TokenStore()
        return secure_store


class EventStreamBindingSpec(pinject.BindingSpec):
    def provide_error_subject(self):
        return rx.subject.Subject()

    def provide_accounts_updated_subject(self):
        return rx.subject.Subject()

    def provide_authenticated_subject(self):
        return rx.subject.Subject()

    def provide_selected_state(self):
        return rx.subject.BehaviorSubject(None)


class AppBindingSpec(pinject.BindingSpec):
    '''wrap all binding specs'''

    def dependencies(self):
        return [StoreBindingSpec(), HttpApiBindingSpec(), DatabaseBindingSpec(), BasicBindingSpec(),
                EventStreamBindingSpec()]
