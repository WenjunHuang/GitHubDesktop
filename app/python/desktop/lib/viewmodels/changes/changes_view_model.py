from enum import IntEnum
from typing import Dict, Iterable, Any, List, Optional

import pinject
from PyQt5.QtCore import QAbstractItemModel, Qt, QModelIndex, Q_ENUM, QAbstractListModel, pyqtProperty, pyqtSignal, \
    pyqtSlot
from PyQt5.QtQuick import QQuickItem
from rx.subject import Subject

from desktop.lib.checkbox import CheckboxValue
from desktop.lib.git.status import WorkingDirectoryFileChange, AppFileStatusKind
from desktop.lib.models.conflict_state import RebaseConflictState
from desktop.lib.models.possible_selections import PossibleSelections, RepositorySelection
from desktop.lib.models.repository import Repository
from desktop.lib.models.working_directory_status import WorkingDirectoryStatus
from desktop.object_graph import get_object_graph


class Roles(IntEnum):
    Include = 0
    File = 1
    FileStatus = 2


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
                         change_files: Iterable[WorkingDirectoryFileChange]):
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
            return self._list[index.row()].status.kind.name.lower()


class ChangesViewModelDependencies:
    def __init(self, selected_state_subject: Subject):
        self.selected_state_subject = selected_state_subject


class ChangesViewModel(QQuickItem):
    includeAllChanged = pyqtSignal()
    disableAllCheckChange = pyqtSignal()

    Q_ENUM(AppFileStatusKind)
    Q_ENUM(CheckboxValue)

    def __init__(self, parent=None):
        super().__init__(parent)
        obj_graph: pinject.object_graph = get_object_graph()
        self._dependencies = obj_graph.provide(ChangesViewModelDependencies)

        self._disposable = self._dependencies.selected_state_subject.subscribe(
            on_next=self.on_working_repository_changed)

        self.destroyed.connect(self.on_destroyed)

        self._change_file_list_model = ChangeFileList(self)

    def on_selected_state_changed(self, selected_state: Optional[PossibleSelections]):
        if not selected_state or type(selected_state) != RepositorySelection:
            return
        else:
            working_directory = selected_state.state.changes_state.working_directory
            if type(selected_state.state.changes_state.conflict_state) == RebaseConflictState:
                rebase_conflict_state = selected_state.state.changes_state.conflict_state
            else:
                rebase_conflict_state = None

            is_commiting = selected_state.state.is_committing
            file_count = len(working_directory.files)

            include_all_value = get_include_all_value(working_directory, rebase_conflict_state)
            self.includeAllValue = include_all_value
            self.disableAllCheckChange = file_count == 0 or is_commiting or not rebase_conflict_state

            self._change_file_list_model.clear_all()
            self._change_file_list_model.add_change_files(working_directory.files)

    def on_destroyed(self):
        self._disposable.dispose()

    @pyqtProperty(QAbstractListModel)
    def changeFileListModel(self):
        return self._change_file_list_model

    @pyqtProperty(bool)
    def includeAll(self):
        return self._include_all

    @pyqtProperty(bool)
    def disableAllCheckChange(self):
        return self._disable_all_check_change

    @disableAllCheckChange.setter
    def disableAllCheckChange(self, value: bool):
        self._disable_all_chech_change = value
        self.disableAllCheckChange.emit()

    @pyqtProperty(CheckboxValue)
    def includeAllValue(self):
        return self._include_all_value

    @includeAll.setter
    def includeAllValue(self, value: CheckboxValue):
        self._include_all_value = value
        self.includeAllChanged.emit()

    @pyqtSlot(int)
    def onRowClick(self,number:int):
        pass


def get_include_all_value(working_directory: WorkingDirectoryStatus,
                          rebase_conflict_state: Optional[RebaseConflictState]) -> CheckboxValue:
    if rebase_conflict_state:
        if len(working_directory.files) == 0:
            return CheckboxValue.Off

        only_untracked_files_found = all(f.status.kind == AppFileStatusKind.Untracked for f in working_directory.files)
        if only_untracked_files_found:
            return CheckboxValue.Off

        only_tracked_files_found = all(f.status.kind != AppFileStatusKind.Untracked for f in working_directory.files)
        return CheckboxValue.On if only_tracked_files_found else CheckboxValue.Mixed

    include_all = working_directory.include_all
    if include_all:
        return CheckboxValue.On
    elif include_all == False:
        return CheckboxValue.Off
    else:
        return CheckboxValue.Mixed
