import unittest
import asyncio

from desktop.lib.git.log import get_commits
from desktop.lib.models.repository import Repository


class TestLog(unittest.TestCase):
    def test_get_commits(self):
        repository = Repository(id=0, path='/Users/huangwenjun/Sources/GitHubDesktop', missing=True, github_repository=None)
        result = asyncio.run(get_commits(repository, 'HEAD..765deb954fb4bc7fd4e366c4fbb7f7125abee001', 100))
        print(result)
