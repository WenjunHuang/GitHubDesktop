from dataclasses import dataclass
from typing import List, Tuple

from desktop.lib.git.status import WorkingDirectoryFileChange


@dataclass(frozen=True)
class WorkingDirectoryStatus:
    files: Tuple[WorkingDirectoryFileChange, ...]
    include_all: bool


@dataclass(frozen=True)
class WorkingDirectoryChangesState:
    status: WorkingDirectoryStatus
    name: str = 'WorkingDirectoryChangesState'
