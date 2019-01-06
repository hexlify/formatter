from os.path import isfile
from sys import exit

from frmty import create_arg_parser, create_lexer, Config
from frmty.lexing import Lexer
from frmty.parsing import Parser
from frmty.visiting import Visitor


if __name__ == '__main__':
    parser = create_arg_parser()
    args = parser.parse_args()

    for path in (args.language, args.source):
        if not isfile(path):
            print("{}: file doesn't exist".format(path))
            exit(1)

    with open(args.language) as lang, open(args.source) as src:
        config = Config.create(lang.read())
        lexer = create_lexer(config)
        tokens = lexer.lex(src.read())

    ast = Parser(tokens).parse()
    result = Visitor(config).visit(ast)
    if args.output == '-':
        print(result)
    else:
        with open(args.output, 'w') as f:
            f.write(result)
