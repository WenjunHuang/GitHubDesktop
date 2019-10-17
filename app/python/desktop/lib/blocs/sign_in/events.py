from dataclasses import dataclass


@dataclass
class AuthenticateWithBasicAuthEvent:
    username: str
    password: str
