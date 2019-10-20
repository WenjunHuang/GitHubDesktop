from dataclasses import dataclass, field
from typing import Optional, Union

from typing_extensions import Literal


@dataclass
class BaseProgress:
    value: int
    title: str
    description: Optional[str]


@dataclass
class GenericProgress(BaseProgress):
    kind: Literal['generic'] = field(init=False,
                                     default='generic')


@dataclass
class CheckoutProgress(BaseProgress):
    kind: Literal['checkout'] = field(init=False,
                                      default='checkout')
    target_branch: str


@dataclass
class FetchProgress(BaseProgress):
    kind: Literal['fetch'] = field(init=False,
                                   default='fetch')
    remote: str


@dataclass
class PullProgress(BaseProgress):
    kind: Literal['pull'] = field(init=False,
                                  default='pull')
    remote: str


@dataclass
class PushProgress(BaseProgress):
    kind: Literal['push'] = field(init=False,
                                  default='push')
    remote: str


@dataclass
class CloneProgress(BaseProgress):
    kind: Literal['clone'] = field(init=False,
                                   default='clone')


@dataclass
class RevertProgress(BaseProgress):
    kind: Literal['revert'] = field(init=False,
                                    default='revert')


@dataclass
class RebaseProgress(BaseProgress):
    kind: Literal['rebase'] = field(init=False,
                                    default='rebase')
    current_commit_summary: str
    rebase_commit_count: int
    total_commit_count: int


Progress = Union[GenericProgress,
                 CheckoutProgress,
                 FetchProgress,
                 PullProgress,
                 PushProgress,
                 RevertProgress,
                 RebaseProgress]
