from dataclasses import dataclass, field
from enum import IntEnum, auto
from typing import Union, Mapping, Optional

from typing_extensions import Literal


class ManualConflictResolutionKind(IntEnum):
    Theirs = auto()
    Ours = auto()


@dataclass
class MergeConflictState:
    kind: Literal['kind'] = field(init=False, default='kind')
    current_branch: str
    current_tip: str
    manual_resolutions: Mapping[str, ManualConflictResolutionKind]


@dataclass
class RebaseConflictState:
    kind: Literal['rebase'] = field(init=False, default='rebase')
    current_tip: str
    target_branch: str
    base_branch: Optional[str]
    original_branch_tip: str
    base_branch_tip: str
    manual_resolutions: Mapping[str, ManualConflictResolutionKind]


ConflictState = Union[MergeConflictState, RebaseConflictState]
