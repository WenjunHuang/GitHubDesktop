from typing import Any

from PyQt5.QtQml import QJSValue

from desktop.lib.api import API
from desktop.lib.bloc import Bloc, BlocError
from desktop.lib.blocs.repository import RepositoryNotLoadedState, LoadAccountRepositoryEvent, \
    LoadingAccountRepositoriesState, FailToLoadAccountRepositoriesState, AccountRepositoriesLoadedState, Account
import asyncio


class AccountRepositoryBloc(Bloc):
    def __init__(self):
        super().__init__()

    def initial_state(self) -> Any:
        return RepositoryNotLoadedState()

    async def map_event_to_state(self, event):
        if isinstance(event, LoadAccountRepositoryEvent):
            yield LoadingAccountRepositoriesState()
            api = API(endpoint=event.endpoint, token=event.token)
            try:
                repositories = await api.fetch_repositories()
            except Exception as e:
                yield FailToLoadAccountRepositoriesState(error=str(e))
            else:
                yield AccountRepositoriesLoadedState(repositories=repositories)

    def map_javascript_event(self, event: QJSValue):
        event_type = event.property("event_type")
        if not event_type.isUndefined() and event_type.isString():
            if event_type.toString() == LoadAccountRepositoryEvent.__name__:
                return LoadAccountRepositoryEvent.from_jsvalue(event)
        raise BlocError(f"can not convert javascript object to event object")
