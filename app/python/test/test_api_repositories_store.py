import asyncio
import unittest

from PyQt5.QtCore import pyqtSignal, QObject

from desktop.lib.http import init_http_session, get_http_session
from desktop.lib.models.account import Account, fetch_user
from desktop.lib.stores.api_repositories_store import ApiRepositoriesStore


class FakeAccountStore(QObject):
    update = pyqtSignal(list)

    def __init__(self):
        super().__init__()


class TestApiRepositoriesStore(unittest.TestCase):
    def setUp(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.token = 'bc0706b46ea74b7009c82c2204358d96c04e4680'
        self.endpoint = "https://api.github.com"
        self.api_repositories_store = ApiRepositoriesStore(FakeAccountStore())
        init_http_session()

    def tearDown(self) -> None:
        self.loop.run_until_complete(get_http_session().close())
        self.loop.close()

    def test_load_repositories(self):
        async def work():
            account = await fetch_user(self.endpoint, self.token)
            return await self.api_repositories_store.load_repositories(account)

        def updated(data):
            print('updated')
            print(data)

        self.api_repositories_store.update.connect(updated)
        result = self.loop.run_until_complete(work())
        print(result)
