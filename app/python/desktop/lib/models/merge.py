from dataclasses import dataclass, field
from typing import Optional, Literal, Iterable, Union

from desktop.lib.models.computed_action import ComputedAction


@dataclass
class BlobResult:
    mode: str
    sha: str
    path: str


class MergeEntry:
    context: str
    base: Optional[BlobResult]
    result: Optional[BlobResult]
    our: Optional[BlobResult]
    their: Optional[BlobResult]
    diff: str
    has_conflicts: Optional[bool]


@dataclass
class MergeSuccess:
    kind: Literal[ComputedAction.Clean] = field(init=False,
                                                default=ComputedAction.Clean)
    entries: Iterable[MergeEntry]


@dataclass
class MergeError:
    kind: Literal[ComputedAction.Conflicts] = field(init=False,
                                                    default=ComputedAction.Conflicts)
    conflicted_files: int


@dataclass
class MergeUnsupported:
    kind: Literal[ComputedAction.Invalid] = field(init=False,
                                                  default=ComputedAction.Invalid)


@dataclass
class MergeLoading:
    kind: Literal[ComputedAction.Loading] = field(init=False,
                                                  default=ComputedAction.Loading)


MergeResult = Union[MergeSuccess, MergeError, MergeUnsupported, MergeLoading]
