from asyncio import Queue, create_task
from typing import AsyncGenerator, Any, MutableMapping

from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot
from PyQt5.QtQml import QQmlEngine, QJSValue
from PyQt5.QtQuick import QQuickItem
from rx.subject import BehaviorSubject

from desktop.lib.common import with_logger
from desktop.lib.convert import to_jsobject


class BlocError(Exception):
    def __init__(self, message):
        super().__init__(message)


@with_logger
class Bloc(QObject):
    def __init__(self):
        super().__init__()
        self._event_queue = Queue()
        self._state_subject = BehaviorSubject(self.initial_state())
        create_task(self._bind_state_subject())

    def current_state(self):
        return self._state_subject.value

    def dispose(self):
        self._state_subject.dispose()

    def on_error(self, error):
        pass

    def initial_state(self) -> Any:
        raise NotImplementedError()

    def map_javascript_event(self, event_props: QJSValue) -> Any:
        raise NotImplementedError()

    async def map_event_to_state(self, event) -> AsyncGenerator:
        raise NotImplementedError()

    def dispatch(self, event):
        if type(event) == QJSValue:
            event = self.map_javascript_event(event)
        create_task(self.__dispatch_event(event))

    async def __dispatch_event(self, event):
        await self._event_queue.put(event)

    async def __bind_state_subject(self):
        create_task(self.__transform_events())

    async def __transform_events(self):
        while True:
            event = await self._event_queue.get()
            try:
                async for state in self.map_event_to_state(event):
                    self._state_subject.on_next(state)
            except Exception as e:
                self.on_error(e)

            self._event_queue.task_done()


class BlockProvider(QQuickItem):
    BlocTypes: MutableMapping[str, Bloc] = {}

    @classmethod
    def register(cls, blocCls):
        cls.BlocTypes[blocCls.__name__] = blocCls

    @classmethod
    def create_bloc(cls, name: str):
        blocCls = cls.BlocTypes.get(name, None)
        if not blocCls:
            return blocCls()
        else:
            return None


class BlocBuilder(QQuickItem):
    stateChanged = pyqtSignal('QJSValue', arguments=['state'])

    def __init__(self, parent=None):
        super().__init__(parent)
        self._disposable = None
        self._bloc = None

    def componentComplete(self):
        super().componentComplete()
        if self._bloc:
            self.stateChanged.emit(to_jsobject(self._bloc.current_state()))
        else:
            raise BlocError("No bloc name provided")

    @pyqtProperty(str)
    def blocName(self):
        return self._bloc_name

    @blocName.setter
    def blocName(self, value: str):
        bloc = QQmlEngine.contextForObject(self).contextProperty(value)
        if bloc:
            self._disposable = bloc.state().subscribe(on_next=self.__on_next)
            self._bloc = bloc
        else:
            raise BlocError(f'bloc {value} does not exist in context')

    @pyqtSlot(str)
    @pyqtSlot(str, QJSValue)
    def dispatch(self, args: QJSValue = QJSValue()):
        assert self._bloc, "No bloc provided"
        self._bloc.dispatch(args)

    @pyqtSlot(result='QJSValue')
    def currentState(self):
        assert self._bloc, "No bloc provided"
        # called by qml javascript to get the current state.Maybe null
        return to_jsobject(self._bloc.current_state())

    def __on_next(self, state):
        try:
            js = to_jsobject(state)
            self.stateChanged.emit(js)
        except Exception as e:
            self.logger.error('error in on_next', e)
