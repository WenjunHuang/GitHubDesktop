from dataclasses import field
from enum import Enum, IntEnum
from typing import Union

from typing_extensions import Literal

from desktop.lib.models.branch import Branch


class TipState(IntEnum):
    Unknown = 0
    Unborn = 1
    Detached = 2
    Valid = 3


class UnknownRepository:
    kind: Literal[TipState.Unknown] = field(init=False,
                                            default=TipState.Unknown)


class UnbornRepository:
    kind: Literal[TipState.Unborn] = field(init=False,
                                           default=TipState.Unborn)
    ref: str


class DetachedHead:
    kind: Literal[TipState.Detached] = field(init=False,
                                             default=TipState.Detached)
    current_sha: str


class ValidBranch:
    kind: Literal[TipState.Valid] = field(init=False,
                                          default=TipState.Valid)
    branch: Branch


Tip = Union[UnknownRepository, UnbornRepository, DetachedHead, ValidBranch]


