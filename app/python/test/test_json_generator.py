import unittest
from dataclasses import dataclass, asdict
from typing import List

from dataclasses_json import dataclass_json
from desktop.lib.json import json_generator


@dataclass_json
@dataclass
class NotificationAuditAttachment:
    attachment_id: str
    name: str
    uri: str


@dataclass_json
@dataclass
class NotificationAuditPicture:
    picture_id: str
    uri: str


@dataclass_json
@dataclass
class NotificationAuditUser:
    name: str
    phone: str
    school_name: str
    type_str: str
    user_id: str


@dataclass_json
@dataclass
class NotificationAudit:
    tag_str: str
    tag: str
    status: str
    resource_id: str
    content: str
    created: str
    user: NotificationAuditUser
    pictures: List[NotificationAuditPicture]
    attachments: List[NotificationAuditAttachment]


class TestHttp(unittest.TestCase):
    def test_generate_obj(self):
        user = NotificationAuditUser(name='wenjun', type_str='tag', phone='12345', school_name='xuerersi',
                                     user_id='abcd')
        print(json_generator(user))

    def test_generate_dic(self):
        user = NotificationAuditUser(name='wenjun', type_str='tag', phone='12345', school_name='xuerersi',
                                     user_id='abcd')
        di = asdict(user)
        print(json_generator(di))
