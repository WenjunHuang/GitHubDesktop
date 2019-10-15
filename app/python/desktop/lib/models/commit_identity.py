from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Optional
import re


@dataclass
class CommitIdentity:
    name: str
    email: str
    date: datetime

    # Format is "NAME <EMAIL> DATE"
    # Wenjun Huang <wenjun.huang80@gmail.com> 1475670580 +0800
    @classmethod
    def parse_identity(cls, identity: str) -> Optional['CommitIdentity']:
        m = re.match(r"^(.*?) <(.*?)> (\d+) (\+|-)?(\d{2})(\d{2})", identity)
        if not m:
            return None
        name = m[1]
        email = m[2]
        # date is specified as seconds from the epoch

        tz_sign = -1 if m[4] == '-' else 1
        tz_HH = int(m[5]) * tz_sign
        tz_mm = int(m[6]) * tz_sign
        dt = datetime.fromtimestamp(int(m[3]), timezone(timedelta(hours=tz_HH, minutes=tz_mm)))

        return CommitIdentity(name=name, email=email, date=dt)
