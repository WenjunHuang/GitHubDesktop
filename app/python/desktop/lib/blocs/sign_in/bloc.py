from typing import AsyncGenerator, Any

from PyQt5.QtQml import QJSValue

from desktop.lib.api import create_authorization
from desktop.lib.bloc import Bloc
from .events import *
from .states import *


@dataclass
class SignInBloc(Bloc):
    def initial_state(self) -> Any:
        return InitState()

    def map_javascript_event(self, event_props: QJSValue) -> Any:
        pass

    async def map_event_to_state(self, event) -> AsyncGenerator:
        if type(event) == AuthenticateWithBasicAuthEvent:
            yield AuthenticatingState()
            create_authorization()

