from typing import Mapping
from desktop.lib.git.spawn import git
import re

kFileNameCaptureRe = re.compile(r"(.+):\d+: leftover conflict marker")


async def get_files_with_conflict_markers(repository_path: str) -> Mapping[str, int]:
    args = ['diff', '--check']
    stdout, _ = await git(args, repository_path)

    # result parsing
    output_str = stdout.decode('utf-8')
    captures = []

    for match in kFileNameCaptureRe.finditer(output_str):
        if match:
            captures.append(match[1])

    if not captures:
        return {}

    counted = dict()
    for c in captures:
        counted[c] = counted.setdefault(c, 0) + 1

    return counted
