from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Repository:
    full_name: str
    stars: int
    crawled_at: datetime = None