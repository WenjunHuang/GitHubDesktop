import asyncio
import unittest
import os

from desktop.lib.git.rev_parse import get_top_level_working_directory


class TestRevParse(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_get_top_level_working_directory(self):
        gitdir = asyncio.run(get_top_level_working_directory(os.getenv("TEST_DIR")))
        print(gitdir)
