from typing import *
from dataclasses import dataclass
from pypika import Query, Table, Field




@dataclass(frozen=True)
class MentionableAssociationDB:
    __slots__ = ['id', 'user_id', 'repository_id']
    id: int
    user_id: int
    repository_id: int


UserTable = Table('t_user')
MentionableAssociationTable = Table('t_mentionable_association')


class GitHubUserDatabase:
    pass
