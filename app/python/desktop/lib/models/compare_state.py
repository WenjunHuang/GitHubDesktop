from dataclasses import dataclass, field
from enum import IntEnum, auto
from typing import Union, Literal, Optional, Iterable

from desktop.lib.models.branch import Branch, AheadBehind
from desktop.lib.models.merge import MergeResult
from desktop.lib.stores.comparison_cache import ComparisonCache


class HistoryTabMode(IntEnum):
    History = 0
    Compare = 1


class ComparisonMode(IntEnum):
    Ahead = 0
    Behind = 1


@dataclass
class DisplayHistory:
    kind: Literal[HistoryTabMode.History] = field(init=False,
                                                  default=HistoryTabMode.History)


class CompareBranch:
    kind: Literal[HistoryTabMode.Compare] = field(init=False,
                                                  default=HistoryTabMode.Compare)
    comparison_mode: ComparisonMode
    comparison_branch: Branch
    ahead_behind: AheadBehind


@dataclass
class InferredComparisonBranch:
    branch: Optional[Branch]
    ahead_behind: Optional[AheadBehind]


@dataclass
class CompareState:
    is_diverging_branch_banner_visible: bool
    form_state: Union[DisplayHistory, CompareBranch]
    merge_status: Optional[MergeResult]
    show_branch_list: bool
    filter_text: str
    tip: Optional[str]
    commit_shas: Iterable[str]
    all_branches: Iterable[Branch]
    recent_branches: Iterable[Branch]
    default_branch: Optional[Branch]
    ahead_behind_cache: ComparisonCache
    inferred_comparison_branch: InferredComparisonBranch
