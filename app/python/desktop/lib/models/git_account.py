from dataclasses import dataclass


@dataclass(frozen=True)
class GitAccount:
    login: str
    endpoint: str
