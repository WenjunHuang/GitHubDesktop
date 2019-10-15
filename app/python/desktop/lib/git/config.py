from desktop.lib.git.spawn import spawn_and_complete
from desktop.lib.models.repository import Repository


async def get_config_value(repository: Repository, name: str):
    flags = ['config', '-z', name]
    stdout, stderr, returncode = await spawn_and_complete(flags, repository.path)

    if returncode == 1:
        return None

    output = stdout.decode('utf-8')
    pieces = output.split('\0')
    return pieces[0]
