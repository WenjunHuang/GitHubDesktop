from typing import Mapping
from dataclasses import replace
from desktop.lib.models.commit_identity import CommitIdentity
from desktop.lib.models.repository import Repository
from desktop.lib.models.repository_state import RepositoryState
from desktop.lib.stores.github_user_store import GitHubUserStore


class RepositoryStateCache:
    def __init__(self, github_user_store: GitHubUserStore):
        self._github_user_store = github_user_store
        self._repository_state: Mapping[Repository, RepositoryState] = dict()

    def get(self, repository: Repository) -> RepositoryState:
        existing = self._repository_state.get(repository)
        if existing:
            github_users = self._github_user_store.get_users_for_repository(repository)
            return replace(existing, github_users={**existing.github_users, **github_users})
        new_item = RepositoryState.create_initial_repository_state()
        self._repository_state[repository] = new_item
        return new_item

    def update(self, repository: Repository, **kwargs):
        current_state = self.get(repository)
        for key, value in kwargs:
            setattr(current_state, key, value)
        self._repository_state[repository] = current_state
