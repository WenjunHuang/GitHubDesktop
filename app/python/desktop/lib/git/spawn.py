from typing import List, Tuple
import asyncio


async def spawn_and_complete(args: List[str],
                             path: str) -> Tuple[bytes, bytes]:
    args = ['git', f"--git-dir {path.join(path, '.git')}"] + args
    proc = await asyncio.create_subprocess_shell(' '.join(args),
                                                 stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()

    return stdout, stderr
