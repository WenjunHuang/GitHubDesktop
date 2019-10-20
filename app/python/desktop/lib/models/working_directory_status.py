from dataclasses import dataclass, field, InitVar
from typing import Mapping, Optional, Iterable

from desktop.lib.git.status import WorkingDirectoryFileChange
from desktop.lib.models.diff import DiffSelectionType


@dataclass
class WorkingDirectoryStatus:
    files: Iterable[WorkingDirectoryFileChange] = field(default_factory=list)
    file_index_by_id: Mapping[str, int] = field(init=False, default_factory=dict)
    include_all: Optional[bool] = True

    def __post_init__(self):
        if not self.include_all:
            self.include_all = get_include_all_state(self.files)

            m = {}
            for ix, f in enumerate(self.files):
                m[f.id] = ix
            self.file_index_by_id = m

    def with_include_all_files(self, include_all: bool) -> 'WorkingDirectoryStatus':
        return WorkingDirectoryStatus(files=map(lambda f: f.with_include_all(include_all), self.files),
                                      include_all=True)

    def find_file_with_id(self, id: str) -> Optional[WorkingDirectoryFileChange]:
        ix = self.file_index_by_id.get(id)
        return None if not ix else self.files[ix]

    def find_file_index_by_id(self, id: str) -> int:
        ix = self.file_index_by_id.get(id)
        return ix if ix else -1


def get_include_all_state(files: Iterable[WorkingDirectoryFileChange]) -> Optional[bool]:
    if not len(files):
        return True

    all_selected = all(f.selection.get_selection_type() == DiffSelectionType.All for f in files)
    none_selected = all(f.selection.get_selection_type() == DiffSelectionType.None_ for f in files)

    if all_selected:
        return True
    elif none_selected:
        return False
    else:
        return None
