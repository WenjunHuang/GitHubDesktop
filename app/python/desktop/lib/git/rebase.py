from dataclasses import dataclass
from io import BytesIO
from typing import Optional

from desktop.lib.common import read_text_file_content
from desktop.lib.models.repository import Repository
from aiofile import AIOFile, Reader
import os


@dataclass
class RebaseInternalState:
    target_branch: str
    base_branch_tip: str
    original_branch_tip: str


def is_rebase_head_set(repository: Repository):
    p = os.path.join(repository.path, '.git', 'REBASE_HEAD')
    return os.path.exists(p)


async def get_rebase_internal_state(repository: Repository) -> Optional[RebaseInternalState]:
    is_rebase = is_rebase_head_set(repository)
    if not is_rebase:
        return None

    original_branch_tip = None
    target_branch = None
    base_branch_tip = None
    try:
        original_branch_tip = await read_text_file_content(
            os.path.join(repository.path, '.git', 'rebase-apply', 'orig-head'))
        original_branch_tip = original_branch_tip.strip()

        target_branch = await read_text_file_content(
            os.path.join(repository.path, '.git', 'rebase-apply', 'head-name'))

        if target_branch.startswith('refs/heads/'):
            target_branch = target_branch[11:].strip()

        base_branch_tip = await read_text_file_content(
            os.path.join(repository.path, '.git', 'rebase-apply', 'onto'))
        base_branch_tip = base_branch_tip.strip()
    except:
        pass

    if original_branch_tip and target_branch and base_branch_tip:
        return RebaseInternalState(original_branch_tip=original_branch_tip,
                                   target_branch=target_branch,
                                   base_branch_tip=base_branch_tip)
    else:
        return None
