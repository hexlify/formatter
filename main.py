from frmty.lexing import Lexer


if __name__ == '__main__':
    l = Lexer()
    l.add('NUMBER', r'\d+')
    l.add('MINUS', r'-')
    l.add('PLUS', r'\+')
    l.ignore(r'\s+')

    for t in l.lex('1 + 2   - 9999'):
        print(t)
