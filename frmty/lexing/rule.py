import re
from typing import Match, Optional

from .token_type import TokenType


class Rule:
    def __init__(self, token_type: TokenType, pattern: str, flags: int):
        self.token_type = token_type
        self.regex = re.compile(pattern, flags=flags)

    def matches(self, source: str, start: int) -> Optional[Match[str]]:
        return self.regex.match(source, start)

    def __repr__(self):
        return '{} {}'.format(str(self.token_type), self.regex.pattern)
