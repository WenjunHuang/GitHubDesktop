from enum import IntEnum
from typing import Dict

from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtQuick import QQuickItem


class Roles(IntEnum):
    Selected, File, Kind = range(3)


class ChangeFileList(QAbstractItemModel):

    def __init__(self, parent=None):
        super().__init__(parent)

    def roleNames(self) -> Dict[int, 'QByteArray']:
        roles = dict()
        roles[Roles.Selected.value] = 'selected'
        roles[Roles.File.value] = 'file'
        roles[Roles.Kind.value] = 'kind'


class ChangesViewModel(QQuickItem):
    def __init__(self, parent=None):
        super().__init__(parent)
