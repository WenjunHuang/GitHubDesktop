from typing import *
from dataclasses import dataclass

from aiosqlite import Connection
from pypika import Query, Table, Field

from desktop.lib.api import API, GitHubAccountType
from desktop.lib.models import Account
from desktop.lib.models.github_user import GitHubUser


@dataclass(frozen=True)
class MentionableAssociationDB:
    __slots__ = ['id', 'user_id', 'repository_id']
    id: int
    user_id: int
    repository_id: int


UserTable = Table('t_user')
MentionableAssociationTable = Table('t_mentionable_association')


class GitHubUserDatabase:

    def __init__(self, db: Connection):
        self.db = db

    async def get_by_login(self, account: Account, login: str):
        q = Query.from_(UserTable).select('*').where((UserTable.endpoint == account.endpoint) & (UserTable.login == login))
        cursor = await self.db.execute(q.get_sql())
        data = await cursor.fetchone()

        if data:
            return GitHubUser(id=data.id,
                              endpoint=data.endpoint,
                              email=data.email,
                              login=data.login,
                              avatar_url=data.avatar_url,
                              name=data.name)
        api = API.from_account(account)
        try:
            api_user = await api.fetch_user(login)
        except:
            api_user = None

        if not api_user or api_user.type != GitHubAccountType.User:
            return None
