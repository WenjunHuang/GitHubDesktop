from dataclasses import dataclass

import pinject
from aiosqlite import Connection
from pypika import Query, Table

from desktop.lib.api import API, GitHubAccountType
from desktop.lib.models import Account
from desktop.lib.models.github_user import GitHubUser
from typing import Callable


@dataclass(frozen=True)
class MentionableAssociationDB:
    __slots__ = ['id', 'user_id', 'repository_id']
    id: int
    user_id: int
    repository_id: int


UserTable = Table('t_user')
MentionableAssociationTable = Table('t_mentionable_association')


class GitHubUserDatabase:
    def __init__(self, database: Connection, provide_api: Callable[[str, str], API]):
        self._database = database
        self._provide_api = provide_api

    async def get_by_login(self, account: Account, login: str):
        q = Query.from_(UserTable).select('*').where(
            (UserTable.endpoint == account.endpoint) & (UserTable.login == login))
        cursor = await self._database.execute(q.get_sql())
        data = await cursor.fetchone()

        if data:
            return GitHubUser(id=data.id,
                              endpoint=data.endpoint,
                              email=data.email,
                              login=data.login,
                              avatar_url=data.avatar_url,
                              name=data.name)
        api = self._provide_api(account.endpoint, account.token)
        try:
            api_user = await api.fetch_user(login)
        except:
            api_user = None

        if not api_user or api_user.type != GitHubAccountType.User:
            return None
