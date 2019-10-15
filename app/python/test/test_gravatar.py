from unittest import TestCase

from desktop.lib.gravatar import generate_gravatar_url
from desktop.lib.models.commit_identity import CommitIdentity


class TestGravatar(TestCase):
    def test_generate(self):
        result = generate_gravatar_url("wenjun.huang80@gmail.com")
        print(result)

