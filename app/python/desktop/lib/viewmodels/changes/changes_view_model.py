from enum import IntEnum
from typing import Dict, Iterable, Any, List, Optional

import pinject
from PyQt5.QtCore import QAbstractItemModel, Qt, QModelIndex, Q_ENUM, QAbstractListModel, pyqtProperty
from PyQt5.QtQuick import QQuickItem
from rx.subject import Subject

from desktop.lib.git.status import WorkingDirectoryFileChange, AppFileStatusKind
from desktop.lib.models.repository import Repository
from desktop.object_graph import get_object_graph


class Roles(IntEnum):
    Include = Qt.UserRole + 1
    File = Qt.UserRole + 2
    FileStatus = Qt.UserRole + 3


class ChangeFileList(QAbstractListModel):
    _list: List[WorkingDirectoryFileChange]
    _include: List[bool]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._list = []

    def roleNames(self) -> Dict[int, 'QByteArray']:
        roles = dict()
        roles[Roles.Include.value] = 'include'
        roles[Roles.File.value] = 'file'
        roles[Roles.Kind.value] = 'fileStatus'
        return roles

    def rowCount(self, parent: QModelIndex) -> int:
        return len(self._list)

    def add_change_files(self,
                         change_files:
                         Iterable[WorkingDirectoryFileChange]):
        begin = len(self._list)
        self.beginInsertRows(QModelIndex(), begin, begin + len(change_files))
        self._list.extend(change_files)
        self.endInsertRows()

    def clear_all(self):
        if len(self._list) == 0:
            return

        self.beginRemoveRows(QModelIndex(), 0, len(self._list) - 1)
        self._list.clear()
        self.endRemoveRows()

    def data(self, index: QModelIndex, role: int) -> Any:
        if role == Roles.Include:
            return self._include[index.row()]
        elif role == Roles.File:
            return self._list[index.row()].path
        elif role == Roles.Kind:
            return self._list[index.row()].status.kind


class ChangesViewModelDependencies:
    def __init(self, working_repository_subject: Subject):
        self.working_repository_subject = working_repository_subject


class ChangesViewModel(QQuickItem):
    Q_ENUM(AppFileStatusKind)

    def __init__(self, parent=None):
        super().__init__(parent)
        obj_graph: pinject.object_graph = get_object_graph()
        self._dependencies = obj_graph.provide(ChangesViewModelDependencies)

        self._disposable = self._dependencies.working_repository_subject.subscribe(
            on_next=self.on_working_repository_changed)

        self.destroyed.connect(self.on_destroyed)

        self._change_file_list_model = ChangeFileList(self)

    def on_working_repository_changed(self, working_repository: Optional[Repository]):
        self._change_file_list_model.clear_all()
        if not working_repository:
            return
        else:
            working_repository.


    def on_destroyed(self):
        self._disposable.dispose()

    @pyqtProperty(QAbstractListModel)
    def changeFileListModel(self):
        return self._change_file_list_model
