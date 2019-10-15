from typing import List
import re

from desktop.lib.git.spawn import spawn_and_complete
from desktop.lib.models.repository import Repository

kBinaryListRe = re.compile(r"-\t-\t(?:\0.+\0)?([^\0]*)")


async def get_binary_paths(repository: Repository, ref: str) -> List[str]:
    stdout, _ = await spawn_and_complete(
        ['diff', '--numstat', '-z', ref],
        repository.path)

    captures = []
    for match in kBinaryListRe.finditer(stdout.decode('utf-8')):
        if match:
            captures.append(match[1])
    return captures
