from dataclasses import dataclass, field
from enum import IntEnum, auto, unique
from typing import Iterable, Union

from typing_extensions import Literal

from desktop.lib.git.status import CommittedFileChange


class StashedChangesLoadStates(IntEnum):
    NotLoaded = auto()
    Loading = auto()
    Loaded = auto()


class StashedNotLoadedChange:
    kind: Literal[StashedChangesLoadStates.NotLoaded] = field(init=False, default=StashedChangesLoadStates.NotLoaded)


class StashedLoadingChange:
    kind: Literal[StashedChangesLoadStates.Loading] = field(init=False, default=StashedChangesLoadStates.Loading)


class StashedLoadedChange:
    kind: Literal[StashedChangesLoadStates.Loaded] = field(init=False, default=StashedChangesLoadStates.Loaded)
    files: Iterable[CommittedFileChange]


StashedFileChanges = Union[StashedNotLoadedChange, StashedLoadingChange, StashedLoadedChange]


@dataclass
class StashEntry:
    name: str
    branch_name: str
    stash_sha: str
    files: StashedFileChanges
