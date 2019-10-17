from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class GitHubUser:
    __slots__ = ['id', 'endpoint', 'email', 'login', 'avatar_url', 'name']
    id: Optional[int]
    endpoint: str
    email: str
    login: str
    avatar_url: str
    name: Optional[str]
