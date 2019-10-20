from dataclasses import dataclass
from typing import Optional


@dataclass
class CommitMessage:
    summary: str
    description: Optional[str]


kDefaultCommitMessage = CommitMessage(summary='', description='')
