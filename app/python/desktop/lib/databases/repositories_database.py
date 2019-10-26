from typing import *
from dataclasses import dataclass, replace

from aiosqlite import Connection
from pypika import SQLLiteQuery as Query, Table, Field
from datetime import datetime

from desktop.lib.api import APIRepositoryData, APIBranchData
from desktop.lib.convert import local_now_with_timezone, timestamp_seconds, from_timestamp_to_local
from desktop.lib.models.github_repository import GitHubRepository
from desktop.lib.models.owner import Owner
from desktop.lib.models.repository import Repository


@dataclass(frozen=True)
class OwnerDB:
    id: Optional[int]
    login: str
    endpoint: str


OwnerTable = Table('t_owner')


@dataclass(frozen=True)
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


class RepositoriesDatabase:
    def __init__(self, database: Connection):
        self._database = database

    async def find_github_repository_by_id(self, id: int) -> Optional[GitHubRepository]:
        q = Query().from_(GitHubRepositoryTable).select("*").where(GitHubRepositoryTable.id == id)
        cursor = await self._database.execute(q.get_sql())
        github_repos = await cursor.fetchone()

        if not github_repos:
            return None
        else:
            return await self.build_github_repository(github_repos)

    async def build_github_repository(self, db_repo: Mapping[str, Any]):
        q = Query().from_(OwnerTable).select("*").where(OwnerTable.id == db_repo['owner_id'])
        cursor = await self._database.execute(q.get_sql())
        owner_db = await cursor.fetchone()

        if not owner_db:
            raise Exception(f"Couldn't find the owner for {db_repo['name']}")

        parent_id = db_repo.get('parent_id')
        if parent_id:
            parent = await self.find_github_repository_by_id(parent_id)
        else:
            parent = None

        return GitHubRepository(
            name=db_repo['name'],
            owner=Owner(id=owner_db['id'], endpoint=owner_db['endpoint'], login=owner_db['login']),
            db_id=db_repo['id'],
            private=db_repo['private'],
            html_url=db_repo['html_url'],
            default_branch=db_repo['default_branch'],
            clone_url=db_repo['clone_url'],
            parent=parent
        )

    async def add_repository(self, path: str) -> Repository:
        github_repo = None
        record_id = None

        q = Query().from_(RepositoryTable).select("*").where(RepositoryTable.path == path)
        cursor = await self._database.execute(q.get_sql())
        repos = await cursor.fetchone()

        if repos:
            record_id = repos['id']
            github_repository_id = repos['github_repository_id']
            if github_repository_id:
                github_repo = await self.find_github_repository_by_id(github_repository_id)
        else:
            insert = Query() \
                .into(RepositoryTable) \
                .columns(
                RepositoryTable.github_repository_id,
                RepositoryTable.path,
                RepositoryTable.missing,
                RepositoryTable.last_stash_check_date) \
                .values(None, path, False, None)
            cursor = await self._database.execute(insert.get_sql())
            record_id = cursor.lastrowid

        return Repository(path=path, id=record_id, github_repository=github_repo, missing=False)

    async def upsert_github_repository(self, endpoint: str, api_repository: APIRepositoryData):
        q = Query().from_(GitHubRepositoryTable) \
            .where(GitHubRepositoryTable.clone_url == api_repository.clone_url) \
            .limit(1)
        cursor = await self._database.execute(q.get_sql())
        github_repository = await cursor.fetchone()

        if not github_repository:
            return await self.put_github_repository(endpoint, api_repository)
        else:
            return await self.build_github_repository(github_repository)

    async def put_github_repository(self, endpoint: str, api_repo: APIRepositoryData):
        parent = None
        if api_repo.parent:
            parent = await self.put_github_repository(endpoint, api_repo.parent)

        login = api_repo.owner.login.lower()
        owner = await self.put_owner(endpoint, login)

        q = Query() \
            .from_(GitHubRepositoryTable) \
            .select("*") \
            .where(GitHubRepositoryTable.owner_id == owner.id and GitHubRepositoryTable.name == api_repo.name)

        existing_repo = self._database.execute(q.get_sql())
        if existing_repo:
            id = existing_repo['id']
        else:
            id = None

        insert = Query().into(GitHubRepositoryTable) \
            .columns(GitHubRepositoryTable.id,
                     GitHubRepositoryTable.owner_id,
                     GitHubRepositoryTable.name,
                     GitHubRepositoryTable.private,
                     GitHubRepositoryTable.html_url,
                     GitHubRepositoryTable.default_branch,
                     GitHubRepositoryTable.clone_url,
                     GitHubRepositoryTable.parent_id,
                     GitHubRepositoryTable.last_prune_date) \
            .replace(id, owner.id, api_repo.name, api_repo.private, api_repo.html_url,
                     api_repo.default_branch, api_repo.clone_url, parent.db_id if parent else None,
                     None)
        cursor = await self._database.execute(insert.get_sql())

        if not id:
            id = cursor.lastrowid

        return GitHubRepository(
            db_id=id,
            name=api_repo.name,
            owner=owner,
            private=api_repo.private,
            html_url=api_repo.html_url,
            clone_url=api_repo.clone_url,
            parent=parent,
            default_branch=api_repo.default_branch
        )

    async def put_owner(self, endpoint: str, login: str) -> Owner:
        login = login.lower()

        q = Query().from_(OwnerTable).select("*").where(OwnerTable.endpoint == endpoint and OwnerTable.login == login)
        cursor = await self._database.execute(q.get_sql())
        existing_owner = await cursor.fetchone()
        if existing_owner:
            return Owner(id=existing_owner['id'],
                         endpoint=endpoint,
                         login=login)
        else:
            insert = Query().into(OwnerTable) \
                .columns(OwnerTable.login, OwnerTable.endpoint) \
                .insert(endpoint, login)
            cursor = await self._database.execute(insert.get_sql())
            id = cursor.lastrowid
            return Owner(id=id,
                         endpoint=endpoint,
                         login=login)

    async def get_all(self) -> Iterable[Repository]:
        inflated_repos = []
        q = Query().from_(RepositoryTable).select("*")
        cursor = await self._database.execute(q.get_sql())
        repos = await cursor.fetchall()

        for repo in repos:
            github_repository_id = repo['github_repository_id']
            if github_repository_id:
                github_repository = await self.find_github_repository_by_id(github_repository_id)
            else:
                github_repository = None
            inflated_repo = Repository(
                id=repo['id'],
                github_repository=github_repository,
                missing=repo['missing'],
                path=repo['path'],
            )
            inflated_repos.append(inflated_repo)

        return inflated_repos

    async def remove_repository(self, repo_id: int):
        q = Query().from_(RepositoryTable).delete().where(RepositoryTable.id == repo_id)
        await self._database.execute(q.get_sql())

    async def update_repository_missing(self, repository: Repository, missing: bool) -> Repository:
        assert repository.id
        update = Query().update(RepositoryTable).set(RepositoryTable.missing, missing).where(
            RepositoryTable.id == repository.id)
        await self._database.execute(update.get_sql())

        return replace(repository, missing=missing)

    async def update_repository_path(self, repository: Repository, path: str) -> Repository:
        assert repository.id
        update = Query() \
            .update(RepositoryTable) \
            .set(RepositoryTable.missing, False) \
            .set(RepositoryTable.path, path) \
            .where(RepositoryTable.id == repository.id)
        await self._database.execute(update.get_sql())
        return replace(repository, missing=False, path=path)

    async def update_last_stash_checkdate(self, repository: Repository, dt: datetime = local_now_with_timezone()):
        assert repository.id

        update = Query().update(RepositoryTable) \
            .set(RepositoryTable.last_stash_check_date, timestamp_seconds(dt)) \
            .where(RepositoryTable.id == repository.id)
        await self._database.execute(update.get_sql())

    async def get_last_stash_checkdate(self, repository: Repository) -> Optional[datetime]:
        assert repository.id

        q = Query().from_(RepositoryTable) \
            .select(RepositoryTable.last_stash_check_date) \
            .where(RepositoryTable.id == repository.id)
        cursor = await self._database.execute(q.get_sql())
        data = await cursor.fetchone()
        if data:
            return from_timestamp_to_local(data['last_stash_check_date'])
        else:
            return None

    async def update_github_repository(self, repository: Repository, endpoint: str,
                                       github_repository: APIRepositoryData):
        assert repository.id

        updated_github_repo = await self.put_github_repository(endpoint, github_repository)

        update = Query().update(RepositoryTable) \
            .set(RepositoryTable.github_repository_id, updated_github_repo.db_id) \
            .where(RepositoryTable.id == repository.id)
        await self._database.execute(update.get_sql())

        return replace(repository, github_repository=updated_github_repo)

    async def update_branch_protections(self,
                                        github_repository: GitHubRepository,
                                        protected_branches: Iterable[APIBranchData]):
        assert github_repository.db_id

        delete = Query().from_(ProtectedBranchTable) \
            .delete() \
            .where(ProtectedBranchTable.repo_id == github_repository.db_id)

        if protected_branches:
            insert = Query().into(ProtectedBranchTable) \
                .columns(ProtectedBranchTable.repo_id, ProtectedBranchTable.name) \
                .values(*[(github_repository.db_id, b.name) for b in protected_branches])
            await self._database.execute(insert.get_sql())

    async def update_last_prune_date(self, repository: Repository, dt: datetime):
        assert repository.id
        assert repository.github_repository
        assert repository.github_repository.db_id

        update = Query().update(GitHubRepositoryTable) \
            .set(GitHubRepositoryTable.last_prune_date, timestamp_seconds(dt)) \
            .where(GitHubRepositoryTable.db_id == repository.github_repository.db_id)
        await self._database.execute(update.get_sql())

