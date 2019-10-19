from desktop.lib.models.commit_identity import CommitIdentity
from desktop.lib.models.repository import Repository
from desktop.lib.stores.github_user_store import GitHubUserStore




class RepositoryStateCache:
    def __init__(self,github_user_store:GitHubUserStore):
        self._github_user_store = github_user_store
        self._repository_state:Mapping[str,RepositoryState] = dict()

    def get(self,repository:Repository):