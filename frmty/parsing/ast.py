from frmty.lexing.token import Token

__all__ = ['AST', 'BinOp', 'UnaryOp', 'Num',
           'Compound', 'Assign', 'Var', 'NoOp', 'Function', 'Program']


class AST:
    pass


class BinOp(AST):
    def __init__(self, left: AST, op: Token, right: AST):
        self.left = left
        self.token = self.op = op
        self.right = right


class UnaryOp(AST):
    def __init__(self, op: Token, expr: AST):
        self.token = self.op = op
        self.expr = expr


class Num(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value


class Compound(AST):
    def __init__(self):
        self.children = []


class Program(AST):
    def __init__(self, functions):
        self.children = functions


class Function(AST):
    def __init__(self, name: str, compound: Compound):
        self.name = name
        self.compound_statement = compound


class Assign(AST):
    def __init__(self, left: AST, op: Token, right: AST):
        self.left = left
        self.token = self.op = op
        self.right = right


class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass
