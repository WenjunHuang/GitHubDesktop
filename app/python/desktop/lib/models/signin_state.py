from dataclasses import dataclass, field
from enum import IntEnum
from typing import Optional

from typing_extensions import Literal

from desktop.lib.models import Account
from desktop.lib.two_factor_auth import AuthenticationMode


class SignInMethod(IntEnum):
    Basic = 0
    Web = 1


class SignInStep(IntEnum):
    EndpointEntry = 0
    Authentication = 1
    TwoFactorAuthentication = 2
    Success = 3


@dataclass
class SignInState:
    kind: SignInStep
    error: Optional[Exception]
    loading: bool


@dataclass
class EndpointEntryState(SignInState):
    kind: Literal[SignInStep.EndpointEntry] = field(init=False,
                                                    default=SignInStep.EndpointEntry)


@dataclass
class AuthenticationState(SignInState):
    kind: Literal[SignInStep.Authentication] = field(init=False,
                                                     default=SignInStep.Authentication)
    endpoint: str
    supports_basic_auth: bool
    forgot_password_url: str


@dataclass
class TwoFactorAuthenticationState(SignInState):
    kind: Literal[SignInStep.TwoFactorAuthentication] = field(init=False,
                                                              default=SignInStep.TwoFactorAuthentication)
    endpoint: str
    username: str
    password: str
    type: AuthenticationMode


@dataclass
class SuccessState(SignInState):
    kind: Literal[SignInStep.Success] = field(init=False,
                                              default=SignInStep.Success)


@dataclass
class AuthenticationEvent:
    account: Account
    method: SignInMethod
