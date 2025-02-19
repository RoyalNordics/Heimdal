from dataclasses import dataclass
from datetime import datetime

@dataclass
class Post:
    content: str
    post_time: datetime
    platform: str