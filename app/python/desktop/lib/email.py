from typing import List

from desktop.lib.api import APIEmailData, EmailVisibility


def get_default_email(emails: List[APIEmailData]) -> str:
    if not emails:
        return ''
    return emails[0].email or ''


def is_email_public(email: APIEmailData) -> bool:
    return email.visibility == EmailVisibility.Public
