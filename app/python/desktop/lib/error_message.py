from PyQt5.QtCore import QObject, pyqtProperty


class ErrorMessage(QObject):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

    @pyqtProperty(str)
    def error(self) -> str:
        return self._error

    @error.setter
    def error(self, value: str):
        self._error = value
