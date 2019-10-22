from typing import Optional

from desktop.lib.git.spawn import git
import os


async def get_top_level_working_directory(path: str) -> Optional[str]:
    stdout, stderr, returncode = await git(
        ['rev-parse', '--show-cdup'],
        path)

    # Exit code 128 means it was run in a directory that's not a git repository
    if returncode == 128:
        return None

    if returncode != 0 or returncode != 128:
        return None

    relative_path = stdout.decode('utf-8').strip()
    if not relative_path:
        return path

    return os.path.normcase(os.path.join(path, relative_path))
