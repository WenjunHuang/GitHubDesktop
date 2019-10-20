from dataclasses import dataclass
from typing import Optional, Iterable, Mapping

from desktop.lib.models.branch import Branch
from desktop.lib.models.pull_request import PullRequest
from desktop.lib.models.tip import Tip


@dataclass
class BranchesState:
    tip: Tip
    default_branch: Optional[Branch]
    all_branches: Iterable[Branch]
    recent_branches: Iterable[Branch]
    open_pull_requests: Iterable[PullRequest]
    is_loading_pull_requests: bool
    current_pull_request: Optional[PullRequest]
    pull_with_rebase: Optional[bool]
    rebased_branches: Mapping[str, str]
