from dataclasses import dataclass, field
from enum import IntEnum
from typing import Union, Optional, Iterable, Awaitable, Callable

from typing_extensions import Literal

from desktop.lib.models.branch import Branch
from desktop.lib.models.commit import CommitOneLine
from desktop.lib.models.conflict_state import RebaseConflictState


class RebaseStepKind(IntEnum):
    ChooseBranch = 0
    WarnForcePush = 1
    ShowProgress = 2
    ShowConflicts = 3
    HideConflicts = 4
    ConfirmAbort = 5
    Completed = 6


@dataclass
class ChooseBranchesStep:
    kind: Literal[RebaseStepKind.ChooseBranch] = field(init=False,
                                                       default=RebaseStepKind.ChooseBranch)
    default_branch: Optional[Branch]
    current_branch: Branch
    all_branches: Iterable[Branch]
    recent_branches: Iterable[Branch]
    initial_branch: Optional[Branch]


@dataclass
class WarnForcePushStep:
    kind: Literal[RebaseStepKind.ChooseBranch] = field(init=False,
                                                       default=RebaseStepKind.ChooseBranch)
    base_branch: Branch
    target_branch: Branch
    commits: Iterable[CommitOneLine]


@dataclass
class ShowProgressStep:
    kind: Literal[RebaseStepKind.ShowProgress] = field(init=False,
                                                       default=RebaseStepKind.ShowProgress)
    rebase_action: Optional[Callable[[], Awaitable[None]]]


class ShowConflictsStep:
    kind: Literal[RebaseStepKind.ShowConflicts] = field(init=False,
                                                        default=RebaseStepKind.ShowConflicts)
    conflict_state: RebaseConflictState


@dataclass
class HideConflictsStep:
    kind: Literal[RebaseStepKind.HideConflicts] = field(init=False,
                                                        default=RebaseStepKind.HideConflicts)


@dataclass
class ConfirmAbortStep:
    kind: Literal[RebaseStepKind.ConfirmAbort] = field(init=False,
                                                       default=RebaseStepKind.ConfirmAbort)
    conflict_state: RebaseConflictState


@dataclass
class HideConflictsStep:
    kind: Literal[RebaseStepKind.HideConflicts] = field(init=False,
                                                        default=RebaseStepKind.HideConflicts)


@dataclass
class ConfirmAbortStep:
    kind: Literal[RebaseStepKind.ConfirmAbort] = field(init=False,
                                                       default=RebaseStepKind.ConfirmAbort)
    conflict_state: RebaseConflictState


@dataclass
class CompletedStep:
    kind: Literal[RebaseStepKind.Completed] = field(init=False,
                                                    default=RebaseStepKind.Completed)


RebaseFlowStep = Union[ChooseBranchesStep,
                       WarnForcePushStep,
                       ShowProgressStep,
                       ShowConflictsStep,
                       HideConflictsStep,
                       ConfirmAbortStep,
                       CompletedStep]
