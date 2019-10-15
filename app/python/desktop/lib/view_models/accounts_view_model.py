import asyncio

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtQml import QJSValue, qjsEngine

from desktop.lib.api import APIEmailData
from desktop.lib.common import with_logger
from desktop.lib.convert import to_jsobject
from desktop.lib.models.account import Account
from desktop.lib.stores.accounts_store import AccountsStore


@with_logger
class AccountsViewModel(QObject):
    def __init__(self, accounts_store: AccountsStore, parent=None):
        super().__init__(parent)
        self._accounts_store = accounts_store

    @pyqtSlot(QJSValue, name="getAllAccounts")
    def get_all_accounts(self, callback: QJSValue):
        async def work(callback: QJSValue):
            js_engine = qjsEngine(self)
            try:
                accounts = await self._accounts_store.get_all()
                jsarray = to_jsobject(accounts, js_engine)
                callback.call([jsarray])
            except Exception as e:
                self.logger.error(f'error in get_all_accounts', e)
                error = js_engine.newErrorObject(QJSValue.GenericError, 'error')
                callback.call([error])

        asyncio.create_task(work(QJSValue(callback)))

    async def async_fetch(self, url, callback: QJSValue):
        try:
            async with self.session.get(url) as r:
                result = await r.text()

        except Exception as e:
            result = f"Error: {e}"
        print(result)

        engine = qjsEngine(self)
        result_object = engine.newObject()
        result_object.setProperty("result", QJSValue(result))
        # result = [QJSValue(result)]
        result = [result_object]
        callback.call(result)
