from dataclasses import dataclass
from typing import Optional, Iterable

from desktop.lib.models.commit import CommitOneLine
from desktop.lib.models.git_rebase_progress import GitRebaseProgress
from desktop.lib.models.rebase_flow_step import RebaseFlowStep


@dataclass
class RebaseState:
    step: Optional[RebaseFlowStep]
    progress: Optional[GitRebaseProgress]
    commits: Optional[Iterable[CommitOneLine]]
    user_has_resolved_conflicts: bool
