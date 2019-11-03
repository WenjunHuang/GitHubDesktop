from desktop.lib.git.spawn import git
from desktop.lib.models.repository import Repository


async def get_config_value(repository: Repository, name: str):
    flags = ['config', '-z', name]
    result = await git(flags, repository.path)

    if not result.success():
        return None

    pieces = result.stdout.split('\0')
    return pieces[0]
