from .token_type import TokenType


class Token:
    def __init__(self, type: TokenType, value: str, position: int):
        self.type = type
        self.value = value
        self.position = position

    def __repr__(self):
        return '{} {}'.format(self.type, self.value)
