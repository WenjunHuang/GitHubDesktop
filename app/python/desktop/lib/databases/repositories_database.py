from typing import *
from dataclasses import dataclass
from pypika import Query, Table, Field
from datetime import datetime


@dataclass
class OwnerDB:
    id: Optional[int]
    login: str
    endpoint: str


OwnerTable = Table('t_owner')


@dataclass
class GitHubRepositoryDB:
    id: Optional[int]
    owner_id: int
    name: str
    private: bool
    html_url: str
    default_branch: str
    clone_url: str
    parent_id: Optional[int]
    last_prune_date: datetime


GitHubRepositoryTable = Table('t_github_repository')


@dataclass
class ProtectedBranchDB:
    repo_id: int
    name: str


ProtectedBranchTable = Table('t_protected_branch')


@dataclass
class RepositoryDB:
    id: Optional[int]
    github_repository_id: int
    path: str
    missing: bool
    last_stash_check_date: Optional[datetime]
    is_tutorial_repository: Optional[bool]


RepositoryTable = Table('t_repository')
