from dataclasses import dataclass
from typing import Optional


@dataclass
class GitRebaseProgress:
    value: int
    rebased_commit_count: int
    current_commit_summary: Optional[str]
    total_commit_count: int
