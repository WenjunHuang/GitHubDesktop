from typing import List, Tuple, Optional, Iterable
import asyncio
import os

from desktop.lib.git.errors import GitError, GitErrorRegexes


class GitError(Exception):
    def __init__(self,result:GitResult,args:Iterable[str]):

async def git(args: List[str],
              path: str,
              stdin: Optional[str] = None) -> Tuple[bytes, bytes, int]:
    args = ['git', f"--git-dir {os.path.join(path, '.git')}"] + args
    proc = await asyncio.create_subprocess_shell(' '.join(args),
                                                 stdin=asyncio.subprocess.PIPE,
                                                 stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE)
    if stdin:
        proc.stdin.write(stdin.encode('utf-8'))
        await proc.stdin.drain()

    stdout, stderr = await proc.communicate()
    returncode = proc.returncode

    return stdout, stderr, returncode


def parse_error(stderr: str) -> Optional[GitError]:
    for regex, error in GitErrorRegexes:
        if regex.match(stderr):
            return error
    return None
