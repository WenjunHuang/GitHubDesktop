from dataclasses import dataclass, field
from enum import IntEnum, auto
from typing import List, Iterable, Optional, Union

from typing_extensions import Literal

from desktop.lib.git.status import CommittedFileChange
from desktop.lib.models.diff import Diff


class ChangesSelectionKind(IntEnum):
    WorkingDirectory = auto()
    Stash = auto()


@dataclass
class ChangesWorkingDirectorySelection:
    kind: Literal[ChangesSelectionKind.WorkingDirectory] = field(init=False,
                                                                 default=ChangesSelectionKind.WorkingDirectory)
    selected_file_ids: Iterable[str] = field(default_factory=list)
    diff: Optional[Diff] = None


@dataclass
class ChangesStashSelection:
    kind: Literal[ChangesSelectionKind.Stash] = field(init=False,
                                                      default=ChangesSelectionKind.Stash)
    selected_stashed_file: Optional[CommittedFileChange]
    selected_stashed_file_diff: Optional[Diff]


ChangesSelection = Union[ChangesWorkingDirectorySelection, ChangesStashSelection]
