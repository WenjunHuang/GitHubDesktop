from unittest import TestCase

from desktop.lib.models.commit_identity import CommitIdentity


class TestCommitIdentity(TestCase):
    def test_parse_identity(self):
        value = "Wenjun Huang <wenjun.huang80@gmail.com> 1475670580 +0800"
        result = CommitIdentity.parse_identity(value)
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Wenjun Huang")
        self.assertEqual(result.email, "wenjun.huang80@gmail.com")
