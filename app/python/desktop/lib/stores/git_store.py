from desktop.lib.app_shell import AppShell
from desktop.lib.git.rev_list import rev_range
from desktop.lib.models.repository import Repository

kCommitBatchSize = 100
kLoadingHistoryRequestKey = 'history'
kRecentBranchesLimit = 5

class GitStore:
    def __init__(self,repository:Repository,app_shell:AppShell):
        self._repository = repository
        self._shell = app_shell

        self._history = []
        self._requests_in_fight = set()

    async def reconcile_history(self,merge_base:str):
        if len(self._history) == 0:
            return

        if kLoadingHistoryRequestKey in self._requests_in_fight:
            return

        self._requests_in_fight.add(kLoadingHistoryRequestKey)

        range = rev_range('HEAD',merge_base)

        commits = await self.perform_failable_operation()