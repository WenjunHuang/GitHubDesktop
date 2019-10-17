from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot, Q_ENUM
from PyQt5.QtQuick import QQuickItem

from desktop.lib.api import get_dotcom_api_endpoint, create_authorization, AuthorizationResponseKind, Optional
from desktop.lib.app_store import get_app_store
from desktop.lib.error_message import ErrorMessage
from desktop.lib.stores import Account, pyqtProperty, fetch_user, with_logger
from enum import Enum, IntEnum
import asyncio


class SignInMethod(Enum):
    Basic = 'basic'
    Web = 'web'


class SignInStep(IntEnum):
    EndpointEntry, Authentication, TwoFactorAuthentication, Success = range(4)


@with_logger
class SignInViewModel(QQuickItem):
    didAuthenticate = pyqtSignal(Account, SignInMethod)
    loadingChanged = pyqtSignal()
    kindChanged = pyqtSignal()
    errorChanged = pyqtSignal()

    Q_ENUM(SignInStep)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._app_store = get_app_store()
        self._loading = False

    @pyqtSlot(name='beginDotComSignIn')
    def begin_dotcom_signin(self):
        self._endpoint = get_dotcom_api_endpoint()
        self.kind = SignInStep.Authentication
        self.loading = False
        self.error = None

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
                self.loading = False
                self.type = response.type
                self._username = username
                self._password = password
            elif response.kind == AuthorizationResponseKind.Error:
                self.loading = False
            elif response.kind == AuthorizationResponseKind.Failed:
                if username.index('@') != -1:
                    self.loading = False
                    self.error = 'Incorrect email or password.'
                else:
                    self.loading = False
                    self.error = 'Incorrect email or password.'
            elif response.kind == AuthorizationResponseKind.UserRequiresVerification:
                self.loading = False
                self.error = get_unverified_user_error_message(username)
            elif response.kind == AuthorizationResponseKind.PersonalAccessTokenBlocked:
                self.loading = False
                self.error = 'A personal access token cannot be used to login to GitHub Desktop.'
            elif response.kind == AuthorizationResponseKind.WebFlowRequired:
                self.loading = False
                self.supports_basic_auth = False
                self.kind = SignInStep.Authentication
            else:
                raise Exception(f"Unsupported response:{response}")

        asyncio.create_task(work())

    @pyqtSlot(name="authenticateWithBrowser")
    def authenticate_with_browser(self):
        pass

    @pyqtSlot(str, name="setTwoFactorOTP")
    def set_two_factor_otp(self, otp: str):
        current_kind = self.kind
        if not current_kind or current_kind != SignInStep.TwoFactorAuthentication:
            raise Exception(f'Sign in step {current_kind} not compatible with two factor authentication')

        self.loading = True

        async def work():
            try:
                response = await create_authorization(self._endpoint,
                                                      self._username,
                                                      self._password,
                                                      otp)
            except Exception as e:
                return

            if response.kind == AuthorizationResponseKind.Authorized:
                token = response.token
                account = await fetch_user(self._endpoint, token)
                await self._app_store.account_store.add_account(account)
            elif response.kind == AuthorizationResponseKind.Failed or response.kind == AuthorizationResponseKind.TwoFactorAuthenticationRequired:
                self.loading = False
                self.error = 'Two-factor authentication failed.'
            elif response.kind == AuthorizationResponseKind.Error:
                # todo emit error
                pass
            elif response.kind == AuthorizationResponseKind.UserRequiresVerification:
                pass
            elif response.kind == AuthorizationResponseKind.PersonalAccessTokenBlocked:
                pass
            elif response.kind == AuthorizationResponseKind.WebFlowRequired:
                self.loading = False
                self._supports_basic_auth = False
                self.kind = SignInStep.Authentication
                self.error = None

        asyncio.create_task(work())

    @pyqtProperty(bool, notify=loadingChanged)
    def loading(self) -> bool:
        return self._loading

    @loading.setter
    def loading(self, value: bool):
        self._loading = value
        self.loadingChanged.emit()

    @pyqtProperty(SignInStep, notify=kindChanged)
    def kind(self):
        return self._kind or None

    @kind.setter
    def kind(self, value: Optional[SignInStep]):
        self._kind = value
        self.kindChanged.emit()

    @pyqtProperty(str, notify=errorChanged)
    def error(self) -> Optional[str]:
        return self._error or None

    @error.setter
    def error(self, error: Optional[str]):
        self._error = error
        self.errorChanged.emit()


def get_unverified_user_error_message(login: str) -> str:
    return f"Unable to authenticate. The account {login} is lacking a verified email address. Please sign in to GitHub.com, confirm your email address in the Emails section under Personal settings, and try again."
