from unittest import TestCase

from desktop.lib.git.config import get_config_value
from desktop.lib.models.repository import Repository
import asyncio


class TestGitConfig(TestCase):
    def test_get_config_value(self):
        repository = Repository(id=0, github_repository=None, path="/home/rick/Sources/GitHubDesktop", missing=False)
        print(asyncio.run(get_config_value(repository, "trailer.separators")))
