from typing import *
from dataclasses import dataclass
from pypika import Query, Table, Field


@dataclass
class PullRequestRefDB:
    repo_id: int
    ref: str
    sha: str


@dataclass
class PullRequestDB:
    number: int
    title: str
    created_at: str
    updated_at: str
    head: PullRequestRefDB
    base: PullRequestRefDB
    author: str


@dataclass
class PullRequestsLastUpdatedDB:
    repo_id: int
    last_updated: int


PullRequestTable = Table('t_pull_request')
PullRequestLastUpdatedTable = Table('t_pull_last_updated')
