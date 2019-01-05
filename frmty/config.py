from re import escape

from frmty.lexing import Lexer, Token
from frmty.lexing import TokenType as TT


tt = {
    'PLUS': TT.PLUS,
    'MINUS': TT.MINUS,
    'MUL': TT.MUL,
    'DIV': TT.DIV,
    'POW': TT.POW,
    'LPAREN': TT.LPAREN,
    'RPAREN': TT.RPAREN,
    'ASSIGN': TT.ASSIGN,
    'BEGIN': TT.BEGIN,
    'END': TT.END,
    'SEMI': TT.SEMI,
    'DEF': TT.DEF,
}


class Config:
    def __init__(self, args: dict):
        self.args = args

    def __getitem__(self, arg: TT):
        return self.args[arg]

    @staticmethod
    def create(lang: str):
        lines = filter(
            lambda l: not l.startswith('#') and l.strip() != '',
            lang.split('\n'))
        args = {}
        for l in lines:
            token_name, token_value = l.split()
            if token_name in tt:
                args[tt[token_name]] = token_value
        return Config(args)


def create_lexer(config: Config) -> Lexer:
    lexer = Lexer()
    lexer.ignore(r'\s+')

    for key in config.args:
        pattern = escape(config[key])
        lexer.add(key, pattern)

    lexer.add(TT.ID, r'(\w)(\w|_|\d)+')
    lexer.add(TT.INTEGER, r'\d+')
    lexer.add(TT.EOF, r'$')
    return lexer
