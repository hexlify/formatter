from frmty.lexing import LexerStream
from frmty.lexing import TokenType as TT

from .ast import *


"""
program : function (function)*

function : DEF variable combound_statement

statement_list : statement
               | statement SEMI statement_list

statement : compound_statement
          | assignment_statement
          | empty

compound_statement : BEGIN statement_list END

assignment_statement : variable ASSIGN expr1

empty :

expr1 : expr2 ((PLUS | MINUS) expr2)*

expr2 : expr3 ((MUL | DIV) expr3)*

expr3 : factor (POW factor)*

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
        self.current_token = self.tokens.next_token()

    def check_and_eat(self, token_type: TT):
        if self.current_token.type != token_type:
            raise ParsingError
        self.eat()

    def program(self):
        """
        """
        ...

    def function(self):
        """
        """
        ...

    def statement(self):
        """statement : compound_statement
                     | assignment_statement
                     | empty
        """
        if self.current_token.type == TT.BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == TT.ID:
            node = self.assignment_statement()
        else:
            node = self.empty()

        return node

    def compound_statement(self):
        """compound_statement : BEGIN statement_list END
        """
        self.check_and_eat(TT.BEGIN)
        nodes = self.statement_list()
        self.check_and_eat(TT.END)

        root = Compound()
        root.children = nodes
        return root

    def statement_list(self):
        """statement_list : statement
                          | statement SEMI statement_list
        """
        results = [self.statement()]
        while self.current_token.type == TT.SEMI:
            self.eat()
            results.append(self.statement())

        if self.current_token.type == TT.ID:
            raise ParsingError

        return results

    def assignment_statement(self) -> AST:
        """assignment_statement : variable ASSIGN expr1
        """
        left = self.variable()
        token = self.current_token
        self.eat()
        right = self.expr1()
        return Assign(left, token, right)

    def empty(self) -> AST:
        """empty :
        """
        return NoOp()

    def expr1(self) -> AST:
        """expr1 : expr2 ((PLUS | MINUS) expr2)*
        """
        node = self.expr2()
        while self.current_token.type in (TT.PLUS, TT.MINUS):
            op = self.current_token
            self.eat()
            node = BinOp(left=node, op=op, right=self.expr2())

        return node

    def expr2(self) -> AST:
        """expr2 : expr3 ((MUL | DIV) expr3)*
        """
        node = self.expr3()
        while self.current_token.type in (TT.MUL, TT.DIV):
            op = self.current_token
            self.eat()
            node = BinOp(left=node, op=op, right=self.expr3())

        return node

    def expr3(self) -> AST:
        """expr3 : factor (POW factor)*
        """
        node = self.factor()
        while self.current_token.type == TT.POW:
            op = self.current_token
            self.eat()
            node = BinOp(left=node, op=op, right=self.factor())

        return node

    def factor(self) -> AST:
        """factor : PLUS factor
                  | MINUS factor
                  | INTEGER
                  | LPAREN expr RPAREN
                  | variable
        """
        if self.current_token.type in (TT.PLUS, TT.MINUS):
            token = self.current_token
            self.eat()
            node = UnaryOp(token, self.factor())
        elif self.current_token.type == TT.INTEGER:
            node = Num(self.current_token)  # type: ignore
            self.eat()
        elif self.current_token.type == TT.LPAREN:
            self.eat()
            node = self.expr1()  # type: ignore
            self.eat()
        else:
            return self.variable()

        return node

    def variable(self) -> AST:
        """variable : ID
        """
        node = Var(self.current_token)
        self.check_and_eat(TT.ID)
        return node

    def parse(self) -> AST:
        node = self.compound_statement()
        if self.current_token.type != TT.EOF:
            raise ParsingError

        return node
