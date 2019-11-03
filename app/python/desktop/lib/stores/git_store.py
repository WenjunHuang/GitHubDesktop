from typing import Iterable, Optional

from desktop.lib.app_shell import AppShell
from desktop.lib.common import with_logger
from desktop.lib.git.config import get_config_value
from desktop.lib.git.for_each_ref import get_branches
from desktop.lib.git.log import get_commits
from desktop.lib.git.reflog import get_recent_branches
from desktop.lib.git.refs import get_symbolic_ref
from desktop.lib.git.rev_list import rev_range
from desktop.lib.models.branch import Branch, BranchType
from desktop.lib.models.commit import Commit
from desktop.lib.models.repository import Repository
from desktop.lib.models.tip import Tip

kCommitBatchSize = 100
kLoadingHistoryRequestKey = 'history'
kRecentBranchesLimit = 5


@with_logger
class GitStore:
    def __init__(self, repository: Repository, app_shell: AppShell):
        self._repository = repository
        self._shell = app_shell

        self._history = []
        self._requests_in_fight = set()
        self._commit_lookup = dict()

    async def reconcile_history(self, merge_base: str):
        if len(self._history) == 0:
            return

        if kLoadingHistoryRequestKey in self._requests_in_fight:
            return

        self._requests_in_fight.add(kLoadingHistoryRequestKey)

        range = rev_range('HEAD', merge_base)

        commits = await get_commits(self._repository, range, kCommitBatchSize)
        if not commits:
            return

        existing_history = self._history
        index = existing_history.index(merge_base)
        if index > -1:
            remaining_history = existing_history[:index]
            self._history = [
                *[c.sha for c in commits],
                *remaining_history
            ]

        self.store_commits(commits, True)
        self._requests_in_fight.remove(kLoadingHistoryRequestKey)
        self.emit_update()

    async def load_next_history_batch(self):
        if kLoadingHistoryRequestKey in self._requests_in_fight:
            return

        if not self._history:
            return

        last_sha = self._history[-1]
        request_key = f"history/{last_sha}"
        if request_key in self._requests_in_fight:
            return

        self._requests_in_fight.add(request_key)

        commits = get_commits(self._repository, f"{last_sha}^", kCommitBatchSize)
        if not commits:
            return

        self._history = self._history.extend([c.sha for c in commits])
        self.store_commits(commits, True)
        self._requests_in_fight.remove(request_key)
        self.emit_update()

    async def load_commit_batch(self, commitish: str):
        if kLoadingHistoryRequestKey in self._requests_in_fight:
            return None

        request_key = f"history/compare/{commitish}"
        if request_key in self._requests_in_fight:
            return None

        self._requests_in_fight.add(request_key)
        try:
            commits = get_commits(self._repository, commitish, kCommitBatchSize)
            self.store_commits(commits, False)
        finally:
            self._requests_in_fight.remove(request_key)

    def history(self):
        return self._history

    async def load_branches(self):
        local_and_remote_branches = await get_branches(self._repository)
        recent_branch_names = await get_recent_branches(self._repository, kRecentBranchesLimit)

        if not local_and_remote_branches:
            return

        self._all_branches = self.merge_remote_and_local_branches(local_and_remote_branches)
        self.refresh_default_branch()
        self.refresh_recent_branches(recent_branch_names)
        self.check_pull_with_rebase()

        commits = [b.tip for b in self._all_branches]
        self.emit_new_commits_loaded(commits)
        self.emit_update()

    def merge_remote_and_local_branches(self, branches: Iterable[Branch]) -> Iterable[Branch]:
        local_branches = []
        remote_branches = []
        for branch in branches:
            if branch.type == BranchType.Local:
                local_branches.append(branch)
            elif branch.type == BranchType.Remote:
                remote_branches.append(branch)

        upstream_branches_added = set()
        all_branches_with_upstream = []

        for branch in local_branches:
            all_branches_with_upstream.append(branch)
            if branch.upstream:
                upstream_branches_added.add(branch.upstream)

        for branch in remote_branches:
            if branch.name in upstream_branches_added:
                continue
            all_branches_with_upstream.append(branch)

        return all_branches_with_upstream

    def store_commits(self, commits: Iterable[Commit], emit_update: bool):
        for commit in commits:
            self._commit_lookup[commit.sha] = commit

        if emit_update:
            self.emit_new_commits_loaded(commits)

    async def check_pull_with_rebase(self):
        result = await get_config_value(self._repository, 'pull.rebase')
        if not result:
            self._pull_with_rebase = None
        elif result == 'true':
            self._pull_with_rebase = True
        elif result == 'false':
            self._pull_with_rebase = False
        else:
            self._logger.warn(f"Unexpected value found for pull.rebase in config: {result}")
            self._pull_with_rebase = None

    async def refresh_default_branch(self):
        default_branch_name = self.resolve_default_branch()
        f = filter(lambda b: b.name == default_branch_name, self._all_branches)
        s = sorted(f, key=lambda x: x.type)
        self._default_branch = next(iter(s), None)

    async def resolve_default_branch(self) -> str:
        github_repository = self._repository.github_repository
        if github_repository and github_repository.default_branch:
            return github_repository.default_branch

        if self._current_remote:
            remote_namespace = f"refs/remotes/{self._current_remote.name}/"
            match = await get_symbolic_ref(self._repository,
                                           f"{remote_namespace}HEAD")
            if match and match.startswith(remote_namespace):
                return match[len(remote_namespace)]

        return 'master'

    def refresh_recent_branches(self, recent_branch_names: Optional[Iterable[str]]):
        if not recent_branch_names:
            self._recent_branches = []
            return

        branches_by_name = {b.name: b for b in self._all_branches}
        recent_branches = [b for b in recent_branch_names if b]
        self._recent_branches = recent_branches

    def tip(self) -> Tip:
        return self._tip

    def default_branch(self) -> Optional[Branch]:
        return self._default_branch

    def all_branches(self) -> Iterable[Branch]:
        return list(self._all_branches)

    def recent_branches(self) -> Iterable[Branch]:
        return list(self._recent_branches)

    async def load_local_commits(self, branch: Optional[Branch]):
        if not branch:
            self._local_commits_shas = []
            return

        if branch.upstream:
            range = rev_range(branch.upstream, branch.name)
            local_commits = await get_commits(self._repository, range, kCommitBatchSize)
        else:
            local_commits = await get_commits(self._repository, 'HEAD', kCommitBatchSize, ['--not', '--remotes'])

        if not local_commits:
            return

        self.store_commits(local_commits)
        self._local_commits_shas = [c.sha for c in local_commits]
        self.emit_update()

    def local_commit_shas(self) -> Iterable[str]:
        return self._local_commits_shas

    def store_commits(self,commits:Iterable[Commit],emit_update:bool=False):
        for commit in commits:
            self._commit_lookup[commit.sha] = commit

        if emit_update:
            self.emit_new_commits_loaded(commits)

    async def undo_first_commit(self,repository:Repository):
