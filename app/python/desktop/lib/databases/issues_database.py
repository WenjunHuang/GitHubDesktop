from typing import *
from dataclasses import dataclass
from pypika import Query, Table, Field


@dataclass
class IssueDB:
    id: int
    github_repository_id: int
    number: int
    title: str
    updated_at: Optional[str]


IssueTable = Table('t_issue')


class IssuesDatabase:
    pass
