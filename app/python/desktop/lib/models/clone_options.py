from dataclasses import dataclass
from typing import Optional

from .git_account import GitAccount


@dataclass(frozen=True)
class CloneOptions:
    account: Optional[GitAccount]
    branch: Optional[str]
