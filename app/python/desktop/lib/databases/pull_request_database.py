from typing import *
from dataclasses import dataclass
from pypika import Query, Table, Field


@dataclass(frozen=True)
class PullRequestRefDB:
    repo_id: int
    ref: str
    sha: str


@dataclass(frozen=True)
class PullRequestDB:
    number: int
    title: str
    created_at: str
    updated_at: str
    head: PullRequestRefDB
    base: PullRequestRefDB
    author: str


@dataclass(frozen=True)
class PullRequestsLastUpdatedDB:
    repo_id: int
    last_updated: int


PullRequestTable = Table('t_pull_request')
PullRequestLastUpdatedTable = Table('t_pull_last_updated')
