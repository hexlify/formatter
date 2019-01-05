from frmty.lexing import LexerStream, TokenType
from .ast import *


"""
program : compound_statement DOT

compound_statement : BEGIN statement_list END

statement_list : statement
               | statement SEMI statement_list

statement : compound_statement
          | assignment_statement
          | empty

assignment_statement : variable ASSIGN expr

empty :

expr1: expr2 ((PLUS | MINUS) expr2)*

expr2: expr3 ((MUL | DIV) expr3)*

expr3: factor (POW factor)*

factor : PLUS factor
       | MINUS factor
       | INTEGER
       | LPAREN expr RPAREN
       | variable

variable: ID
"""


class ParsingError(Exception):
    pass


class Parser:
    def __init__(self, tokens: LexerStream):
        self.tokens = tokens
        self.current_token = self.tokens.next_token()

    def eat(self):
        # if self.current_token.token_type != token_type:
        #     raise ParsingError

        self.current_token = self.tokens.next_token()

    def program(self):
        ...

    def compound_statement(self):
        ...

    def statement_list(self):
        ...

    def statement(self):
        ...

    def assignment_statement(self):
        ...

    def empty(self):
        ...

    def expr1(self) -> AST:
        """expr1: expr2 ((PLUS | MINUS) expr2)*
        """
        node = self.expr2()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token
            self.eat()
            node = BinOp(left=node, op=op, right=self.expr2())

        return node

    def expr2(self) -> AST:
        """expr3 ((MUL | DIV) expr3)*
        """
        node = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            op = self.current_token
            self.eat()
            node = BinOp(left=node, op=op, right=self.factor())

        return node

    def expr3(self) -> AST:
        """expr3: factor (POW factor)*
        """
        ...

    def factor(self) -> AST:
        """factor : PLUS factor
                  | MINUS factor
                  | INTEGER
                  | LPAREN expr RPAREN
                  | variable
        """
        if self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            self.eat()
            node = UnaryOp(token, self.factor())
        elif self.current_token.type == TokenType.INTEGER:
            node = Num(self.current_token)  # type: ignore
            self.eat()
        elif self.current_token.type == TokenType.LPAREN:
            self.eat()
            node = self.expr1()  # type: ignore
            self.eat()
        else:
            return self.variable()

        return node

    def variable(self) -> AST:
        """variable: ID
        """
        if self.current_token.type != TokenType.ID:
            raise ParsingError
        node = Var(self.current_token)
        self.eat()
        return node

    def parse(self) -> AST:
        node = self.expr1()
        if self.current_token.type != TokenType.EOF:
            raise ParsingError

        return node
