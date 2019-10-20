from dataclasses import dataclass
from typing import Iterable, Union, Mapping, Optional

from desktop.lib.models import Account
from desktop.lib.models.cloning_repository import CloningRepository
from desktop.lib.models.local_repository_state import LocalRepositoryState
from desktop.lib.models.possible_selections import PossibleSelections
from desktop.lib.models.repository import Repository
from desktop.lib.models.signin_state import SignInState


@dataclass
class AppState:
    accounts: Iterable[Account]
    repositories: Iterable[Union[Repository, CloningRepository]]
    local_repository_state_lookup: Mapping[int, LocalRepositoryState]
    selected_state: Optional[PossibleSelections]
    signin_state: Optional[SignInState]
