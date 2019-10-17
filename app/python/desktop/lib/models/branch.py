from dataclasses import dataclass
from typing import Optional, Tuple
from enum import IntEnum, Enum
import re

from desktop.lib.models.commit import Commit


class BranchType(IntEnum):
    Local = 0
    Remote = 1


class StartPoint(Enum):
    CurrentBranch = 'CurrentBranch'
    DefaultBranch = 'DefaultBranch'
    Head = 'Head'


@dataclass(frozen=True)
class AheadBehind:
    ahead: int
    behind: int


@dataclass(frozen=True)
class CompareResult(AheadBehind):
    commits: Tuple[Commit, ...]


@dataclass(frozen=True)
class Branch:
    name: str
    upstream: Optional[str]
    tip: Commit
    type: BranchType

    def remote(self) -> Optional[str]:
        upstream = self.upstream
        if not upstream:
            return None

        pieces = re.match(r"(.*?)/.*", upstream)
        if not pieces:
            return None
        else:
            return pieces[1]

    def upstream_without_remote(self) -> Optional[str]:
        if not self.upstream:
            return None

        return remove_remote_prefix(self.upstream)

    def name_without_remote(self) -> Optional[str]:
        if self.type == BranchType.Local:
            return self.name
        else:
            without_remote = remove_remote_prefix(self.name)
            return without_remote or self.name

    def eligible_for_fast_forward(self, current_branch_name: Optional[str]) -> bool:
        return self.type == BranchType.Local and self.name != current_branch_name and self.upstream


def remove_remote_prefix(name: str) -> Optional[str]:
    pieces = re.match(r".*?/(.*)", name)
    if not pieces:
        return None
    return pieces[1]
