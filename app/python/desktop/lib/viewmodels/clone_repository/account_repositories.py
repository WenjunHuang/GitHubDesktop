from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot
from PyQt5.QtQuick import QQuickItem


class AccountRepositoriesViewModel(QQuickItem):
    loading = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtProperty(bool)
    def loading(self):
        return self.loading or False

    @loading.setter
    def loading(self, value: bool):
        self.loading = value

    @pyqtSlot(name='reload')
    def reload(self):
        self.loading = True
