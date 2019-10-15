from typing import *
from dataclasses import dataclass
from pypika import Query, Table, Field


@dataclass
class GitHubUserDB:
    id: Optional[int]
    endpoint: str
    email: str
    login: str
    avatar_url: str
    name: Optional[str]


@dataclass
class MentionableAssociationDB:
    id: int
    user_id: int
    repository_id: int


UserTable = Table('t_user')
MentionableAssociationTable = Table('t_mentionable_association')


class GitHubUserDatabase:
    pass
