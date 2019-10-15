from dataclasses import dataclass
from typing import Optional, Union, Mapping

from desktop.lib.api import get_dotcom_api_endpoint
from desktop.lib.databases.github_user_database import GitHubUser
from desktop.lib.gravatar import generate_gravatar_url
from .commit_identity import CommitIdentity
from .github_repository import GitHubRepository
from .git_author import GitAuthor
from urllib import parse


@dataclass
class AvatarUser:
    email: str
    avatar_url: str
    name: str


def get_fallback_avatar_url_for_author(github_repository: Optional[GitHubRepository],
                                       author: Union[CommitIdentity, GitAuthor]):
    if github_repository and github_repository.endpoint() == get_dotcom_api_endpoint():
        return f"https://avatars.githubusercontent.com/u/e?email={parse.quote(author.email)}&s=60"
    else:
        return generate_gravatar_url(author.email)


def get_avatar_user_from_author(github_repository: Optional[GitHubRepository],
                                github_users: Optional[Mapping[str, GitHubUser]],
                                author: Union[CommitIdentity, GitAuthor]) -> AvatarUser:
    github_user = None if not github_users else github_users.get(author.email.lower())
    avatar_url = github_user.avatar_url if github_user else get_fallback_avatar_url_for_author(github_repository,
                                                                                               author)
    return AvatarUser(email=author.email,
                      name=author.name,
                      avatar_url=avatar_url)

def get_avatar_users_for_commit(github_repository:Optional[GitHubRepository],
                                github_users:Optional[Mapping[str,GitHubUser]],
                                commit:Commit):
