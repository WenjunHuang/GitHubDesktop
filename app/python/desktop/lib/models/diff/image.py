from dataclasses import dataclass


@dataclass
class Image:
    contents: str
    media_type: str
    bytes: int
