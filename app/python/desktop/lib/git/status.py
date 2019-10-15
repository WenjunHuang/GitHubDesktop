import itertools
import logging
import re
from collections import deque
from dataclasses import dataclass, field, InitVar
from enum import Enum
from typing import *
from typing_extensions import Literal

from desktop.lib.git.diff import get_binary_paths
from desktop.lib.git.diff_check import get_files_with_conflict_markers
from desktop.lib.git.merge import is_mergeheadset
from desktop.lib.git.rebase import get_rebase_internal_state, RebaseInternalState
from desktop.lib.git.spawn import spawn_and_complete
from desktop.lib.models.repository import Repository


class GitStatusEntry(Enum):
    Modified = 'M'
    Added = 'A'
    Deleted = 'D'
    Renamed = 'R'
    Copied = 'C'
    Unchanged = '.'
    Untracked = '?'
    Ignored = '!'
    UpdatedButUnmerged = 'U'


class AppFileStatusKind(Enum):
    New = 'New'
    Modified = 'Modified'
    Deleted = 'Deleted'
    Copied = 'Copied'
    Renamed = 'Renamed'
    Conflicted = 'Conflicted'
    Untracked = 'Untracked'


class UnmergedEntrySummary(Enum):
    AddedByUs = 'added-by-us'
    DeletedByUs = 'deleted-by-us'
    AddedByThem = 'added-by-them'
    DeletedByThem = 'deleted-by-them'
    BothDeleted = 'both-delected'
    BothAdded = 'both-added'
    BothModified = 'both-modified'


class OrdinaryEntryType(Enum):
    Added = 'added'
    Modified = 'modified'
    Deleted = 'deleted'


@dataclass
class UnmergedEntry:
    action: UnmergedEntrySummary
    us: GitStatusEntry
    them: GitStatusEntry


@dataclass
class OrdinaryEntry:
    type: OrdinaryEntryType
    index: Optional[GitStatusEntry] = None
    working_tree: Optional[GitStatusEntry] = None


@dataclass
class PlainFileStatus:
    kind: Literal[AppFileStatusKind.New, AppFileStatusKind.Modified, AppFileStatusKind.Deleted]


class TextConflictEntry:
    kind: Literal[AppFileStatusKind.Conflicted]
    action: UnmergedEntrySummary
    us: GitStatusEntry
    them: GitStatusEntry


@dataclass
class ConflictedFileStatus:
    kind: Literal[AppFileStatusKind.Conflicted]
    entry: TextConflictEntry
    conflict_marker_count: Optional[int] = None


@dataclass
class CopiedOrRenamedFileStatus:
    kind: Literal[AppFileStatusKind.Copied, AppFileStatusKind.Renamed]
    old_path: str


@dataclass
class UntrackedFileStatus:
    kind: Literal[AppFileStatusKind.Untracked]


AppFileStatus = Union[PlainFileStatus, CopiedOrRenamedFileStatus, ConflictedFileStatus, UntrackedFileStatus]


@dataclass
class UntrackedEntry:
    pass


@dataclass
class RenamedEntry:
    index: Optional[GitStatusEntry]
    working_tree: Optional[GitStatusEntry]


@dataclass
class CopiedEntry:
    index: Optional[GitStatusEntry]
    working_tree: Optional[GitStatusEntry]


FileEntry = Union[OrdinaryEntry, RenamedEntry, CopiedEntry, UnmergedEntry, UntrackedEntry]


@dataclass
class StatusHeader:
    value: str


@dataclass
class StatusEntry:
    path: str
    status_code: str
    old_path: Optional[str]


StatusItem = Union[StatusHeader, StatusEntry]
kConflictStatusCode = ['DD', 'AU', 'UD', 'UA', 'DU', 'AA', 'UU']


async def get_status(repository: Repository):
    args = [
        '--no-optional-locks',
        'status',
        '--untracked-files=all',
        '--branch',
        '--porcelain=2',
        '-z',
    ]
    stdout, stderr = spawn_and_complete(args, repository.path)

    if stdout:
        parsed = parse_porcelain_status(stdout.decode())
        headers = itertools.takewhile(lambda i: type(i) == StatusItem, parsed)
        entries = itertools.takewhile(lambda i: type(i) == StatusEntry, parsed)
        merge_head_found = is_mergeheadset(repository)

        conflicted_files_in_index = any([i.status_code in kConflictStatusCode for i in entries])
        rebase_internal_state = await get_rebase_internal_state(repository)
        conflict_details = await get_conflict_details(repository, merge_head_found,
                                                      conflicted_files_in_index,
                                                      rebase_internal_state)
        files = entries
    if stderr:
        raise Exception(f'[stderr]\n{stderr.decode()}')


def map_status(status: str) -> FileEntry:
    if status == '??':
        return UntrackedEntry()

    if status == '.M':
        return OrdinaryEntry(type=OrdinaryEntryType.Modified,
                             index=GitStatusEntry.Unchanged,
                             working_tree=GitStatusEntry.Modified)

    if status == 'M.':
        return OrdinaryEntry(type=OrdinaryEntryType.Modified,
                             index=GitStatusEntry.Modified,
                             working_tree=GitStatusEntry.Unchanged)

    if status == '.A':
        return OrdinaryEntry(type=OrdinaryEntryType.Added,
                             index=GitStatusEntry.Unchanged,
                             working_tree=GitStatusEntry.Added)

    if status == 'A.':
        return OrdinaryEntry(type=OrdinaryEntryType.Added,
                             index=GitStatusEntry.Added,
                             working_tree=GitStatusEntry.Unchanged)

    if status == '.D':
        return OrdinaryEntry(type=OrdinaryEntryType.Deleted,
                             index=GitStatusEntry.Unchanged,
                             working_tree=GitStatusEntry.Deleted)

    if status == 'D.':
        return OrdinaryEntry(type=OrdinaryEntryType.Deleted,
                             index=GitStatusEntry.Deleted,
                             working_tree=GitStatusEntry.Unchanged)

    if status == 'R.':
        return RenamedEntry(index=GitStatusEntry.Renamed,
                            working_tree=GitStatusEntry.Unchanged)

    if status == '.R':
        return RenamedEntry(index=GitStatusEntry.Unchanged,
                            working_tree=GitStatusEntry.Renamed)

    if status == 'C.':
        return CopiedEntry(index=GitStatusEntry.Copied,
                           working_tree=GitStatusEntry.Unchanged)

    if status == '.C':
        return CopiedEntry(index=GitStatusEntry.Unchanged,
                           working_tree=GitStatusEntry.Copied)

    if status == 'AD':
        return OrdinaryEntry(type=OrdinaryEntryType.Added,
                             index=GitStatusEntry.Added,
                             working_tree=GitStatusEntry.Deleted)

    if status == 'AM':
        return OrdinaryEntry(type=OrdinaryEntryType.Added,
                             index=GitStatusEntry.Added,
                             working_tree=GitStatusEntry.Modified)

    if status == 'RM':
        return RenamedEntry(index=GitStatusEntry.Renamed,
                            working_tree=GitStatusEntry.Modified)

    if status == 'RD':
        return RenamedEntry(index=GitStatusEntry.Renamed,
                            working_tree=GitStatusEntry.Deleted)

    if status == 'DD':
        return UnmergedEntry(action=UnmergedEntrySummary.BothDeleted,
                             us=GitStatusEntry.Deleted,
                             them=GitStatusEntry.Deleted)

    if status == 'AU':
        return UnmergedEntry(action=UnmergedEntrySummary.AddedByUs,
                             us=GitStatusEntry.Added,
                             them=GitStatusEntry.UpdatedButUnmerged)

    if status == 'UD':
        return UnmergedEntry(action=UnmergedEntrySummary.DeletedByThem,
                             us=GitStatusEntry.UpdatedButUnmerged,
                             them=GitStatusEntry.Deleted)

    if status == 'UA':
        return UnmergedEntry(action=UnmergedEntrySummary.AddedByThem,
                             us=GitStatusEntry.UpdatedButUnmerged,
                             them=GitStatusEntry.Added)

    if status == 'DU':
        return UnmergedEntry(action=UnmergedEntrySummary.DeletedByUs,
                             us=GitStatusEntry.Deleted,
                             them=GitStatusEntry.UpdatedButUnmerged)

    if status == 'AA':
        return UnmergedEntry(action=UnmergedEntrySummary.BothAdded,
                             us=GitStatusEntry.Added,
                             them=GitStatusEntry.Added)

    if status == 'UU':
        return UnmergedEntry(action=UnmergedEntrySummary.BothModified,
                             us=GitStatusEntry.UpdatedButUnmerged,
                             them=GitStatusEntry.UpdatedButUnmerged)

    return OrdinaryEntry(type=OrdinaryEntryType.Modified)


@dataclass
class ConflictFilesDetails:
    conflict_counts_by_path: Mapping[str, int] = field(default_factory=dict)
    binary_file_paths: List[str] = field(default_factory=list)


async def get_conflict_details(repository: Repository,
                               merge_head_found: bool,
                               lookfor_stash_conflicts: bool,
                               rebase_internal_state: Optional[RebaseInternalState]
                               ) -> ConflictFilesDetails:
    try:
        if merge_head_found:
            return await get_merge_conflict_details(repository)
        if rebase_internal_state:
            return await get_rebase_conflict_details(repository)
        if lookfor_stash_conflicts:
            return await get_working_directory_conflict_details(repository)
    except Exception as e:
        logging.error('Unexpected error from git operations in get_conflict_details', e)

    return ConflictFilesDetails()


async def get_merge_conflict_details(repository: Repository):
    conflict_counts_by_path = await get_files_with_conflict_markers(repository.path)
    binary_file_paths = await get_binary_paths(repository, 'MERGE_HEAD')
    return ConflictFilesDetails(conflict_counts_by_path=conflict_counts_by_path,
                                binary_file_paths=binary_file_paths)


async def get_rebase_conflict_details(repository: Repository):
    conflict_counts_by_path = await get_files_with_conflict_markers(repository.path)
    binary_file_paths = await get_binary_paths(repository, 'REBASE_HEAD')
    return ConflictFilesDetails(conflict_counts_by_path=conflict_counts_by_path,
                                binary_file_paths=binary_file_paths)


async def get_working_directory_conflict_details(repository: Repository):
    conflict_counts_by_path = await get_files_with_conflict_markers(repository.path)
    binary_file_paths = []
    try:
        binary_file_paths = await get_binary_paths(repository, 'HEAD')
    except:
        pass
    return ConflictFilesDetails(conflict_counts_by_path=conflict_counts_by_path,
                                binary_file_paths=binary_file_paths)


@dataclass
class FileChange:
    id: str = field(init=False)
    path: InitVar[str]
    status: InitVar[AppFileStatus]

    def __post_init__(self, path: str, status: AppFileStatus):
        if status.kind == AppFileStatusKind.Renamed or status.kind == AppFileStatusKind.Copied:
            self.id = f"{status.kind.value}+{path}+{status.old_path}"
        else:
            self.id = f"{status.kind.value}+{path}"

@dataclass
class WorkingDirectoryFileChange(FileChange):
    selection:DiffSelection




def build_status_map(files: MutableMapping[str, WorkingDirectoryFileChange])


kChangeEntryType = '1'
kRenamedOrCopiedEntryType = '2'
kUnmergedEntryType = 'u'
kUntrackedEntryType = '?'
kIgnoredEntryType = '!'

kChangedEntryRe = re.compile(
    "^1 ([MADRCUTX?!.]{2}) (N\.\.\.|S[C.][M.][U.]) (\d+) (\d+) (\d+) ([a-f0-9]+) ([a-f0-9]+) ([\s\S]*?)$")


def parse_changed_entry(field: str) -> StatusEntry:
    match = kChangedEntryRe.match(field)
    if not match:
        raise Exception(f'Failed to parse status line for changed entry: ${field}')
    else:
        return StatusEntry(status_code=match[1], path=match[8])


kRenamedOrCopiedEntryRe = re.compile(
    "^2 ([MADRCUTX?!.]{2}) (N\.\.\.|S[C.][M.][U.]) (\d+) (\d+) (\d+) ([a-f0-9]+) ([a-f0-9]+) ([RC]\d+) ([\s\S]*?)$")


def parsed_renamed_or_copied_entry(field: str, old_path: Optional[str]) -> StatusEntry:
    match = kRenamedOrCopiedEntryRe.match(field)
    if not match:
        raise Exception(f'Failed to parse status line for renamed or copied entry: ${field}')
    else:
        if not old_path:
            raise Exception(f'Failed to parse renamed or copied entry, could not parse old path')
        return StatusEntry(status_code=match[1], old_path=old_path, path=match[9])


kUnmergedEntryRe = re.compile(
    "^u ([DAU]{2}) (N\.\.\.|S[C.][M.][U.]) (\d+) (\d+) (\d+) (\d+) ([a-f0-9]+) ([a-f0-9]+) ([a-f0-9]+) ([\s\S]*?)$")


def parse_unmerged_entry(field: str) -> StatusEntry:
    match = kUnmergedEntryRe.match(field)

    if not match:
        raise Exception(f"Failed to parse status line for unmerged entry: {field}")
    else:
        return StatusEntry(status_code=match[1], path=match[10])


def shift(queue: deque):
    try:
        left = queue.popleft()
    except IndexError:
        return None
    else:
        return left


def parse_porcelain_status(output: str) -> List[StatusItem]:
    tokens = output.split('\0')
    queue = deque(tokens)
    entries: List[StatusItem] = []

    field = shift(queue)

    while field:
        if field.startswith('# ') and len(field) > 2:
            entries.append(StatusHeader(value=field[2:]))
        else:
            entry_kind = field[0:1]
            if entry_kind == kChangeEntryType:
                entries.append(parse_changed_entry(field))
            elif entry_kind == kRenamedOrCopiedEntryType:
                entries.append(parsed_renamed_or_copied_entry(field, shift(queue)))
            elif entry_kind == kUnmergedEntryType:
                entries.append(parse_unmerged_entry(field))
            elif entry_kind == kIgnoredEntryType:
                pass

        field = shift(queue)
    return entries
