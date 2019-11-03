from dataclasses import dataclass

ForkedRemotePrefix = 'github-desktop-'


def fork_pull_request_remote_name(remote_name: str):
    return f"{ForkedRemotePrefix}{remote_name}"


@dataclass
class Remote:
    name: str
    url: str
