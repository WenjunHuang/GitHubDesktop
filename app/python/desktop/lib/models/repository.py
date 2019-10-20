from dataclasses import dataclass, field, InitVar
from typing import Optional
import pathlib

from desktop.lib.models.github_repository import GitHubRepository


@dataclass
class Repository:
    '''A local repository'''
    id: int
    github_repository: Optional[GitHubRepository]
    missing: bool
    name: str = field(init=False)
    path: str

    def __post_init__(self):
        if self.github_repository and self.github_repository.name:
            self.name = self.github_repository.name
        else:
            self.name = get_base_name(self.path)


def get_base_name(path: str) -> str:
    base_name = pathlib.Path(path).name
    return base_name
