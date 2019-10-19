from dataclasses import dataclass
from typing import Optional, Iterable

from desktop.lib.git.status import CommittedFileChange
from desktop.lib.models.diff import Diff


@dataclass
class CommitSelection:
    sha: Optional[str]
    changed_files: Iterable[CommittedFileChange]
    file: Optional[CommittedFileChange]
    diff: Optional[Diff]
