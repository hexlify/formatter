from .rule import Rule
from .token import Token


class LexingError(Exception):
    pass


class Lexer:
    def __init__(self):
        self.rules = []
        self.ignore_rules = []

    def add(self, name: str, pattern: str, flags=0):
        self.rules.append(Rule(name, pattern, flags))

    def ignore(self, pattern: str, flags=0):
        self.ignore_rules.append(Rule('-', pattern, flags))

    def lex(self, source: str):
        return LexerStream(self, source)


class LexerStream:
    def __init__(self, lexer: Lexer, source: str):
        self.lexer = lexer
        self.source = source
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            if self.index >= len(self.source):
                raise StopIteration
            for ignore in self.lexer.ignore_rules:
                match = ignore.matches(self.source, self.index)
                if match is not None:
                    self.index = match.end()
                    break
            break

        for rule in self.lexer.rules:
            match = rule.matches(self.source, self.index)
            if match is not None:
                token = Token(
                    rule.name,
                    self.source[match.start():match.end()],
                    match.start())
                self.index = match.end()
                return token

        raise LexingError()
