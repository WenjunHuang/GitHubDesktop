from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Iterable

from desktop.lib.git.interpret_trailers import Trailer
from desktop.lib.models.commit_identity import CommitIdentity
from desktop.lib.models.git_author import GitAuthor


@dataclass(frozen=True)
class CommitContext:
    __slots__ = ['summary', 'description', 'trailers']
    summary: str
    description: Optional[str]
    trailers: Optional[List[Trailer]]


@dataclass(frozen=True)
class CommitOneLine:
    __slots__ = ['sha', 'summary']
    sha: str
    summary: str


@dataclass(frozen=True)
class Commit:
    coauthors: List[GitAuthor] = field(init=False)
    authored_by_commiter: bool = field(init=False)
    sha: str
    short_sha: str
    summary: str
    body: str
    author: CommitIdentity
    committer: CommitIdentity
    parent_shas: Tuple[str, ...]
    trailers: Tuple[Trailer, ...]

    def __post_init__(self):
        object.__setattr__(self, 'coauthors', extract_coauthors(self.trailers))
        object.__setattr__(self, 'authored_by_commiter',
                           self.author.name == self.committer.name and self.author.email == self.committer.email)


def extract_coauthors(trailers: Iterable[Trailer]) -> Iterable[GitAuthor]:
    coauthors = []

    for trailer in trailers:
        if trailer.is_coauthors():
            author = GitAuthor.parse(trailer.value)
            if author:
                coauthors.append(author)

    return coauthors
