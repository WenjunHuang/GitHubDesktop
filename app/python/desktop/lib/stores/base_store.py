from typing import Any

from PyQt5.QtCore import QObject, pyqtSignal
from pyee import BaseEventEmitter


class BaseStore(QObject):
    update = pyqtSignal(object)
    error = pyqtSignal(Exception)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._emitter = BaseEventEmitter()

    def emit_update(self, data):
        self.update.emit(data)

    def emit_error(self, error: Exception):
        self.error.emit(error)
