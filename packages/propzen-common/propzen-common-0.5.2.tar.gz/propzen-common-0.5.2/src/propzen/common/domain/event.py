import time
from dataclasses import dataclass, field


@dataclass
class Event:
    timestamp: float = field(default_factory=time.time, init=False)
