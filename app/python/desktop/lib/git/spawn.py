from typing import List, Tuple, Optional, Iterable
import asyncio
import os

from desktop.lib.git.errors import GitErrorRegexes, GitCmdStatusCode


async def git(args: List[str],
              path: str,
              stdin: Optional[str] = None) -> Tuple[bytes, bytes, int]:
    # args = [f"--git-dir {path}"] + args
    try:
        proc = await asyncio.create_subprocess_exec('git', *args,
                                                    stdin=asyncio.subprocess.PIPE,
                                                    stdout=asyncio.subprocess.PIPE,
                                                    stderr=asyncio.subprocess.PIPE,
                                                    cwd=path)
        if stdin:
            proc.stdin.write(stdin.encode('utf-8'))
            await proc.stdin.drain()

        stdout, stderr = await proc.communicate()
        returncode = proc.returncode

        return stdout, stderr, returncode
    except FileNotFoundError as e:
        return None, None, GitCmdStatusCode.GitNotFoundErrorCode


def parse_error(stderr: str) -> Optional[GitCmdStatusCode]:
    for regex, error in GitErrorRegexes:
        if regex.match(stderr):
            return error
    return None
