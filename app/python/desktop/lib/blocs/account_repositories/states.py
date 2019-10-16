from dataclasses import dataclass
from typing import List

from desktop.lib.api import APIRepositoryData
from desktop.lib.models import Account


@dataclass
class RepositoryNotLoadedState:
    name: str = 'RepositoryNotLoadedState'


@dataclass
class LoadingAccountRepositoriesState:
    name: str = 'LoadingAccountRepositoriesState'


@dataclass
class AccountRepositoriesLoadedState:
    repositories: List[APIRepositoryData]
    name: str = 'AccountRepositoriesLoadedState'


@dataclass
class FailToLoadAccountRepositoriesState:
    error: str
    name: str = 'FailToLoadAccountRepositoriesState'
