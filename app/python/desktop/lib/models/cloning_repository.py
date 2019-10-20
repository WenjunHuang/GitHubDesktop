from dataclasses import dataclass, field
import os


@dataclass
class CloningRepository:
    id: int
    path: str
    url: str
    name: str = field(init=False)

    def __post_init__(self):
        if self.url.endswith('.git'):
            url = self.url[0:-4]
        else:
            url = self.url
        self.name = os.path.basename(url)
