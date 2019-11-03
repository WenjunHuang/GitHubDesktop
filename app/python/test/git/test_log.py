import unittest
import asyncio

from desktop.lib.git.log import get_commits
from desktop.lib.models.repository import Repository


class TestLog(unittest.TestCase):
    def test_get_commits(self):
        repository = Repository(id=0, path='/home/rick/Sources/GitHubDesktop', missing=True, github_repository=None)
        result = asyncio.run(get_commits(repository, '38ccd784d21b8e15621045cad63576279ddda913..HEAD', 100))
        print(result)
