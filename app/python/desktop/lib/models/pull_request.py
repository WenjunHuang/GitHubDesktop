from dataclasses import dataclass
from datetime import datetime

from desktop.lib.api import APIRefState
from desktop.lib.models.github_repository import GitHubRepository


@dataclass
class PullRequestRef:
    ref: str
    sha: str
    github_repository: GitHubRepository


@dataclass
class CommitStatus:
    id: int
    state: APIRefState
    description: str


@dataclass
class PullRequest:
    created: datetime
    title: str
    pull_request_number: int
    head: PullRequestRef
    base: PullRequestRef
    author: str
