from typing import Any

from desktop.lib.api import API
from desktop.lib.bloc import Bloc, BlocError
from .events import *
from .states import *


class AccountRepositoriesBloc(Bloc):
    def __init__(self, account: Account):
        super().__init__()
        self.account = account

    def initial_state(self) -> Any:
        self.dispatch(LoadAccountRepositoriesEvent())
        return RepositoryNotLoadedState()

    async def map_event_to_state(self, event):
        if isinstance(event, LoadAccountRepositoriesEvent):
            yield LoadingAccountRepositoriesState()
            api = API(endpoint=self.account.endpoint, token=self.account.token)
            try:
                repositories = await api.fetch_repositories()
            except Exception as e:
                yield FailToLoadAccountRepositoriesState(error=str(e))
            else:
                yield AccountRepositoriesLoadedState(repositories=repositories)

    def map_javascript_event(self, event: QJSValue):
        event_type = event.property("event_type")
        if not event_type.isUndefined() and event_type.isString():
            if event_type.toString() == LoadAccountRepositoriesEvent.__name__:
                return LoadAccountRepositoriesEvent.from_jsvalue(event)
        raise BlocError(f"can not convert javascript object to event object")
