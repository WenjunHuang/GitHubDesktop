from dataclasses import dataclass
from typing import Optional

from .github_repository import GitHubRepository


@dataclass
class AvatarUser:
    email: str
    avatar_url: str
    name: str

def get_fallback_avatar_url_for_author(github_repository:Optional[GitHubRepository],
                                       author:Union[CommitIdentity,GitAuthor]):

