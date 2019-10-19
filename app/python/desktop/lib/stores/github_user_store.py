from typing import Set, Mapping

from desktop.lib.api import get_dotcom_api_endpoint
from desktop.lib.databases.github_user_database import GitHubUserDatabase
from desktop.lib.models.github_user import GitHubUser
from desktop.lib.models.repository import Repository


class GitHubUserStore:
    def __init__(self, github_user_database: GitHubUserDatabase):
        self._database = github_user_database
        self._requests_in_flight: Set[str] = set()
        self._users_by_endpoint: Mapping[str, Mapping[str, GitHubUser]] = dict()

    def get_users_for_repository(self, repository: Repository) -> Mapping[str, GitHubUser]:
        endpoint = repository.github_repository or get_dotcom_api_endpoint()
        return self.get_users_for_endpoint(endpoint) or dict()

    def get_users_for_endpoint(self, endpoint):
        return self._users_by_endpoint.get(endpoint)
