from dataclasses import dataclass
from typing import Optional
import pathlib

from desktop.lib.models.github_repository import GitHubRepository


@dataclass
class Repository:
    '''A local repository'''
    id: int
    github_repository: Optional[GitHubRepository]
    missing: bool
    path: str

    def name(self):
        if self.github_repository and self.github_repository.name:
            return self.github_repository.name
        else:
            return get_base_name(self.path)


def get_base_name(path: str) -> str:
    base_name = pathlib.Path(path).name
    return base_name
