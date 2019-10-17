from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from typing_extensions import Literal


class BannerType(Enum):
    SuccessfulMerge = 'SuccessfulMerge'
    MergeConflictsFound = 'MergeConflictsFound'
    SuccessfulRebase = 'SuccessfulRebase'
    RebaseConflictsFound = 'RebaseConflictsFound'


@dataclass(frozen=True)
class SuccessfulMergeBanner:
    type: Literal[BannerType.SuccessfulMerge] = field(init=False, default=BannerType.SuccessfulMerge)
    our_branch: str
    their_branch: Optional[str]


@dataclass(frozen=True)
class MergeConflictsFoundBanner:
    type: Literal[BannerType.MergeConflictsFound]
    our_branch: str
    popup: Popup
