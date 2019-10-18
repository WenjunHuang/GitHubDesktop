from enum import IntEnum
from typing import Dict

from PyQt5.QtCore import QAbstractItemModel, Qt, QModelIndex
from PyQt5.QtQuick import QQuickItem

from desktop.lib.git.status import WorkingDirectoryFileChange


class Roles(IntEnum):
    Include = Qt.UserRole + 1
    File = Qt.UserRole + 2
    Kind = Qt.UserRole + 3


class ChangeFileList(QAbstractItemModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._list = []

    def roleNames(self) -> Dict[int, 'QByteArray']:
        roles = dict()
        roles[Roles.Include.value] = 'selected'
        roles[Roles.File.value] = 'file'
        roles[Roles.Kind.value] = 'kind'

    def rowCount(self, parent: QModelIndex) -> int:
        return len(self._list)

    def add_change_file(self,change_file:WorkingDirectoryFileChange):
        self.beginInsertRows()


class ChangesViewModel(QQuickItem):
    def __init__(self, parent=None):
        super().__init__(parent)
