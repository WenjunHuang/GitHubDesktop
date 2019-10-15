from desktop.lib.models.repository import Repository
from os import path


def is_mergeheadset(repository: Repository)->bool:
    p = path.join(repository.path, '.git', 'MERGE_HEAD')
    return path.exists(p)
