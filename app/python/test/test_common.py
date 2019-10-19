import asyncio
import unittest

import aiohttp

from desktop.lib.api import API, IssueState, create_authorization
from desktop.lib.common import read_text_file_content
from desktop.lib.http import request, HTTPMethod, deserialize_object, init_http_session, get_http_session
from desktop.lib.models.account import fetch_user


class TestCommon(unittest.TestCase):
    def setUp(self) -> None:
        self.loop = asyncio.get_event_loop()

    def test_read_file_content(self):
        result = self.loop.run_until_complete(read_text_file_content("./test_common.py"))
        print(result)
