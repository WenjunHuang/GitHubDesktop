from dataclasses import dataclass
from typing import Optional

from desktop.lib.models.branch import AheadBehind


@dataclass
class LocalRepositoryState:
    ahead_behind: Optional[AheadBehind]
    changed_files_count: int
