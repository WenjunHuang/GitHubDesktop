import unittest
import asyncio

from desktop.lib.git.for_each_ref import get_branches
from desktop.lib.models.repository import Repository


class TestForEachRef(unittest.TestCase):
    def test_get_branches(self):
        repository = Repository(id=0, github_repository=None, path='/home/rick/Sources/GitHubDesktop', missing=False)
        result = asyncio.run(get_branches(repository))
        print(result)
