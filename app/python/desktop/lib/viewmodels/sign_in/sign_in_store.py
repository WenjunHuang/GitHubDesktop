from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot, Q_ENUM
from PyQt5.QtQuick import QQuickItem

from desktop.lib.api import get_dotcom_api_endpoint, create_authorization, AuthorizationResponseKind
from desktop.lib.app_store import get_app_store
from desktop.lib.stores import Account, pyqtProperty, fetch_user
from enum import Enum, IntEnum
import asyncio


class SignInMethod(Enum):
    Basic = 'basic'
    Web = 'web'


class SignInStep(IntEnum):
    EndpointEntry, Authentication, TwoFactorAuthentication, Success = range(4)


class SignInViewModel(QQuickItem):
    didAuthenticate = pyqtSignal(Account, SignInMethod)
    loadingChanged = pyqtSignal()
    kindChanged = pyqtSignal()

    Q_ENUM(SignInStep)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._app_store = get_app_store()

    @pyqtSlot(name='beginDotComSignIn')
    def begin_dotcom_signin(self):
        self._endpoint = get_dotcom_api_endpoint()
        self._kind = SignInStep.Authentication
        self.kindChanged.emit()

        pass

    @pyqtSlot(str, str, name='authenticateWithBasicAuth')
    def authenticate_with_basic_auth(self, username: str, password: str):
        self.loading = True

        async def work():
            response = await create_authorization(self._endpoint, username, password)
            if response.kind == AuthorizationResponseKind.Authorized:
                token = response.token
                account = await fetch_user(self._endpoint, token)
                await self._app_store.account_store.add_account(account)

                self.kind = SignInStep.Success
                self.loading = False
            elif response.kind == AuthorizationResponseKind.TwoFactorAuthenticationRequired:
                self.kind = SignInStep.TwoFactorAuthentication
                self._username = username
                self._password = password
                self.type =

    @pyqtProperty(bool, notify=loadingChanged)
    def loading(self) -> bool:
        return self._loading

    @loading.setter
    def loading(self, value: bool):
        self._loading = value
        self.loadingChanged.emit()

    @pyqtProperty(SignInStep, notify=kindChanged)
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, value: SignInStep):
        self._kind = value
        self.kindChanged.emit()
