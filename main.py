from os.path import isfile
from sys import exit

from frmty.arg_parser import create_parser
from frmty.lexing import Lexer, TokenType
from frmty.parsing import Parser
from frmty.visiting import Visitor


def configure_lexer(lang_description: str) -> Lexer:
    lexer = Lexer()
    lexer.ignore(r'\s+')
    lexer.add(TokenType.PLUS, r'\+')
    lexer.add(TokenType.MINUS, r'-')
    lexer.add(TokenType.MUL, r'\*')
    lexer.add(TokenType.DIV, r'/')
    lexer.add(TokenType.LPAREN, r'\(')
    lexer.add(TokenType.RPAREN, r'\)')
    lexer.add(TokenType.INTEGER, r'\d+')
    lexer.add(TokenType.ID, r'\w+')
    lexer.add(TokenType.ASSIGN, r':=')
    lexer.add(TokenType.EOF, r'$')
    return lexer

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    for path in (args.language, args.source):
        if not isfile(path):
            print("{}: file doesn't exist".format(path))
            exit(1)

    with open(args.language) as lang, open(args.source) as src:
        lexer = configure_lexer(lang.read())
        tokens = lexer.lex(src.read())

    ast = Parser(tokens).parse()
    result = Visitor().visit(ast)
    print(result)
