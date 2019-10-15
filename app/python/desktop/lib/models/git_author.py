from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class GitAuthor:
    name: str
    email: str

    @classmethod
    def parse(cls, name_addr: str) -> Optional['GitAuthor']:
        m = re.match(r"^(.*?)\s+<(.*?)>", name_addr)
        return None if not m else GitAuthor(name=m[1], email=m[2])
