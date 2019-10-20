from dataclasses import dataclass, field
from enum import IntEnum
from typing import Union

from typing_extensions import Literal

from desktop.lib.models.baseprogress import CloneProgress
from desktop.lib.models.cloning_repository import CloningRepository
from desktop.lib.models.repository import Repository
from desktop.lib.models.repository_state import RepositoryState


class SelectionType(IntEnum):
    Repository = 0
    CloningRepository = 1
    MissingRepository = 2


@dataclass
class RepositorySelection:
    kind: Literal[SelectionType.Repository] = field(init=False,
                                                    default=SelectionType.Repository)
    repository: Repository
    state: RepositoryState


@dataclass
class CloningRepositorySelection:
    kind: Literal[SelectionType.CloningRepository] = field(init=False,
                                                           default=SelectionType.CloningRepository)
    repository: CloningRepository
    progress: CloneProgress


@dataclass
class MissingRepositorySelection:
    kind: Literal[SelectionType.MissingRepository] = field(init=False,
                                                           default=SelectionType.MissingRepository)
    repository: Repository


PossibleSelections = Union[RepositorySelection,
                           CloningRepositorySelection,
                           MissingRepositorySelection]
