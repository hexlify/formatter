from enum import Enum


class TokenType(Enum):
    IGNORE = -1

    PLUS = 0
    MINUS = 1
    MUL = 2
    DIV = 3
    POW = 4
    LPAREN = 5
    RPAREN = 6

    INTEGER = 7
    ID = 8

    ASSIGN = 9

    BEGIN = 10,
    END = 11,
    SEMI = 12,

    EOF = 99
