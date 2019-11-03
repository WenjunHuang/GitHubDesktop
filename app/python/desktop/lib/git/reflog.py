from typing import Container

from desktop.lib.git.spawn import git
from desktop.lib.models.repository import Repository
import re


async def get_recent_branches(repository: Repository, limit: int) -> Container[str]:
    regex = re.compile(
        r".*? (renamed|checkout)(?:: moving from|\s*) (?:refs/heads/|\s*)(.*?) to (?:refs/heads/|\s*)(.*?)$")
    result = await git([
        'log',
        '-g',
        '--no-abbrev-commit',
        '--pretty=oneline',
        'HEAD',
        '-n',
        '2500',
        '--'],
        repository.path)

    if result.return_code == 128:
        # error code 128 is returned if the branch is unborn
        return []

    lines = result.stdout.split('\n')
    names = set()
    exclude_names = set(['master'])

    for line in lines:
        result = regex.search(line)
        if result:
            operation_type = result[1]
            exclude_branch_name = result[2]
            branch_name = result[3]

            if operation_type == 'renamed':
                exclude_names.add(exclude_branch_name)

            if branch_name not in exclude_names:
                names.add(branch_name)
        if len(names) == limit:
            break

    return [*names]
