from argparse import ArgumentParser


def create_arg_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('language', help="Language description file")
    parser.add_argument('source', help="Source file")

    return parser
