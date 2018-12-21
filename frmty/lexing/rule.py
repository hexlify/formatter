import re
from typing import Match, Optional


class Rule:
    def __init__(self, name: str, pattern: str, flags: int):
        self.name = name
        self.regex = re.compile(pattern, flags=flags)

    def matches(self, source: str, start: int) -> Optional[Match[str]]:
        return self.regex.match(source, start)
