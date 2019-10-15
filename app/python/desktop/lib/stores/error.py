from PyQt5.QtCore import QObject, pyqtProperty


class Error(QObject):
    def __init__(self, message: str):
        super().__init__()
        self._message = message

    @pyqtProperty(str)
    def message(self):
        return self._message

    @message.setter
    def message(self, value: str):
        self._message = value
