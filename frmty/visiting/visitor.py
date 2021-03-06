import typing as t

from frmty.lexing import Token
from frmty.lexing import TokenType as TT
from frmty.parsing.ast import *
from frmty import Config


precedencies = {
    TT.PLUS: 1,
    TT.MINUS: 1,
    TT.MUL: 2,
    TT.DIV: 2,
    TT.POW: 3
}


class VisitorError(Exception):
    def __init__(self, message: str):
        self.message = message


class NodeVisitor:
    def visit(self, node: AST) -> str:
        method_name = 'visit_' + type(node).__name__
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise VisitorError('No visit_{} method'.format(type(node).__name__))


class Visitor(NodeVisitor):
    def __init__(self, config: Config):
        self.config = config

    def visit_BinOp(self, node: BinOp) -> str:
        results = []  # type: t.List[str]
        for n in (node.left, node.right):
            n_str = self.visit(n)
            if self.__need_parentheses(n, node):
                n_str = self.config[TT.LPAREN] + n_str + self.config[TT.RPAREN]
            results.append(n_str)

        return '{} {} {}'.format(results[0], node.op.value, results[1])

    def visit_UnaryOp(self, node: UnaryOp) -> str:
        if node.op.type == TT.MINUS:
            return '-' + self.visit(node.expr)
        return self.visit(node.expr)

    def visit_Num(self, node: Num) -> str:
        return str(node.value)

    def visit_Compound(self, node: Compound) -> str:
        res = self.config[TT.BEGIN] + '\n'
        for c in node.children[:-1]:
            res += '\t{}{}\n'.format(self.visit(c), self.config[TT.SEMI])
        if len(node.children) == 1:
            res += '\n'
        res += self.config[TT.END] + '\n'

        return res

    def visit_Program(self, node: Program) -> str:
        return '\n\n'.join(self.visit(c) for c in node.children)

    def visit_Function(self, node: Function) -> str:
        return 'function {}\n'.format(node.name) \
               + self.visit_Compound(node.compound_statement)

    def visit_Assign(self, node: Assign) -> str:
        left = self.visit(node.left)
        right = self.visit(node.right)
        return '{} {} {}'.format(left, node.op.value, right)

    def visit_Var(self, node: Var) -> str:
        return node.value

    def visit_NoOp(self, node: NoOp) -> str:
        return ''

    def __need_parentheses(self, node: AST, current_op: BinOp):
        return (isinstance(node, BinOp) or
                (isinstance(node, UnaryOp) and node.op.type == TT.MINUS)) \
            and precedencies[node.op.type] < precedencies[current_op.op.type]
