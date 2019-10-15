from dataclasses import dataclass
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
    type: Literal[BannerType.SuccessfulMerge]
    our_branch: str
    their_branch: Optional[str]

class
