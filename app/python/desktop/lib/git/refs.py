from typing import Optional

from desktop.lib.git.spawn import git, GitExecutionOptions
from desktop.lib.models.repository import Repository


async def get_symbolic_ref(repository: Repository, ref: str) -> Optional[str]:
    result = await git(['symbolic-ref', '-q', ref],
                       repository.path,
                       GitExecutionOptions(
                           success_return_codes={0, 1, 128}
                       ))
    if result.return_code == 1 or result.return_code == 128:
        #  - 1 is the exit code that Git throws in quiet mode when the ref is not a
        # symbolic ref
        #  - 128 is the generic error code that Git returns when it can't find
        #  something
        return None
    return result.stdout.strip()
