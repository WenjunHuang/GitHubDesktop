from typing import AsyncGenerator, Any

from PyQt5.QtQml import QJSValue

from desktop.lib.bloc import Bloc


class CurrentRepositoryBloc(Bloc):
    def initial_state(self) -> Any:
        pass

    def map_javascript_event(self, event_props: QJSValue) -> Any:
        pass

    async def map_event_to_state(self, event) -> AsyncGenerator:
        pass