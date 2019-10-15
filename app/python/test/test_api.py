import asyncio
import unittest

import aiohttp

from desktop.lib.api import API, IssueState, create_authorization
from desktop.lib.http import request, HTTPMethod, deserialize_object, init_session, get_session
from desktop.lib.models.account import fetch_user


class TestHttp(unittest.TestCase):
    def setUp(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.token = 'c415e9d535a95a28ecf955c01487330ebfa646e7'
        self.endpoint = "https://api.github.com"
        init_session()

    def tearDown(self) -> None:
        self.loop.run_until_complete(get_session().close())
        self.loop.close()

    async def get_result(self):
        response = await request(
            get_session(),
            'http://192.168.2.243',
            None,
            HTTPMethod.GET,
            '/notification/backstage_audit/audit_notifications')
        result = await deserialize_object(response, PagingResult)
        return result

    def test_request(self):
        result = self.loop.run_until_complete(self.get_result())
        print(result)

    def test_fetch_repositories(self):
        api = API("https://api.github.com", self.token)
        result = self.loop.run_until_complete(api.fetch_repositories())
        print(result)

    def test_fetch_account(self):
        api = API("https://api.github.com", self.token)
        result = self.loop.run_until_complete(api.fetch_account())
        print(result)

    def test_fetch_emails(self):
        api = API("https://api.github.com", self.token)
        result = self.loop.run_until_complete(api.fetch_emails())
        print(result)

    def test_fetch_commit(self):
        api = API(self.endpoint, self.token)
        result = self.loop.run_until_complete(
            api.fetch_commit('WenjunHuang', 'PythonPlayground', '28e0afd70bf79a4b53cbfc933dedfec838ad34d0'))
        print(result)

    def test_search_for_user_with_email(self):
        api = API(self.endpoint, self.token)
        result = self.loop.run_until_complete(
            api.search_for_user_with_email("tgrabiec@gmail.com"))
        print(result)

    def test_fetch_orgs(self):
        api = API(self.endpoint, self.token)
        result = self.loop.run_until_complete(
            api.fetch_orgs())
        print(result)

    def test_create_repository(self):
        api = API(self.endpoint, self.token)
        try:
            result = self.loop.run_until_complete(
                api.create_repository(None, "WenjunTestCreate", "WenjunTestCreate", False))
            print(result)
        except Exception as e:
            print(e)

    def test_fetch_issues(self):
        api = API(self.endpoint, self.token)
        result = self.loop.run_until_complete(
            api.fetch_issues("shiftkey", "desktop", IssueState.All))

        print(result)

    def test_fetch_all_open_pull_requests(self):
        api = API(self.endpoint, self.token)
        result = self.loop.run_until_complete(
            api.fetch_all_open_pull_requests("shiftkey", "desktop"))

        print(result)

    def test_fetch_protected_branches(self):
        api = API(self.endpoint, self.token)
        loop = asyncio.get_event_loop()
        task = loop.create_task(api.fetch_protected_branches("WenjunHuang", "WebFontendPlayground"))
        result = self.loop.run_until_complete(
            api.fetch_protected_branches("WenjunHuang", "WebFontendPlayground"))
        print(result)

        result = loop.run_until_complete(task)
        print(result)

    def test_fetch_account(self):
        result = self.loop.run_until_complete(fetch_user(self.endpoint, self.token))
        print(result.id)
        for email in result.emails:
            print(email.email)
            print(email.visibility)

    def test_create_authorization(self):
        result = self.loop.run_until_complete(create_authorization(self.endpoint, "WenjunHuang", "Rick198023"))
        print(result)
