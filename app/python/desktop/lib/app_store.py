from dataclasses import dataclass
from typing import Optional, List

from PyQt5.QtCore import QObject, pyqtProperty

from desktop.lib.models import Account
from desktop.lib.models.repository import Repository


class AppStore(QObject):
    def __init__(self, github_user_store: GitHubUserStore,
                 accounts_store: AccountsStore):
        super().__init__()

        self.github_user_store = github_user_store
        self.accounts_store = accounts_store

    async def load_initial_state(self):
