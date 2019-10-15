from dataclasses import dataclass

# The owner of a GitHubRepository
from typing import Optional


@dataclass
class Owner:
    id: Optional[int]
    login: str
    endpoint: str
