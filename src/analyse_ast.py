# Analyse Comparative Avancée de la Structure du Code en Python

from __future__ import annotations

import ast
from ast import NodeVisitor
from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Feature:
    feature_type: str
    line: int
    column: int
    metadata: str | None


class CodeAST(NodeVisitor):
    """
    Classe pour l'analyse de l'AST de code Python.
    """

    def __init__(self):
        self.features: list[Feature] = []

    def visit_Return(self, node):
        self.features.append(Feature("Return", node.lineno, node.col_offset, None))
        self.generic_visit(node)

    def visit_BinOp(self, node):
        op_type = type(node.op).__name__
        self.features.append(Feature("BinOp", node.lineno, node.col_offset, op_type))
        self.generic_visit(node)

    def visit_For(self, node):
        self.features.append(Feature("For", node.lineno, node.col_offset, None))
        self.generic_visit(node)

    def visit_While(self, node):
        self.features.append(Feature("While", node.lineno, node.col_offset, None))
        self.generic_visit(node)

    def visit_Assign(self, node):
        self.features.append(Feature("Assign", node.lineno, node.col_offset, None))
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        self.features.append(Feature("AnnAssign", node.lineno, node.col_offset, None))
        self.generic_visit(node)

    def visit_Num(self, node):
        self.features.append(Feature("Num", node.lineno, node.col_offset, None))
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.features.append(Feature("FunctionDef", node.lineno, node.col_offset, None))
        self.generic_visit(node)

    def visit_Print(self, node):
        self.features.append(Feature("Print", node.lineno, node.col_offset, node.values))
        self.generic_visit(node)


def compare_codes(code1: str, code2: str):
    code_ast1 = CodeAST()
    code_ast1.visit(ast.parse(code1))

    code_ast2 = CodeAST()
    code_ast2.visit(ast.parse(code2))

    common_features = set(code_ast1.features).intersection(set(code_ast2.features))
    total_features = set(code_ast1.features).union(set(code_ast2.features))

    similarity = len(common_features) / len(total_features) if total_features else 0

    return similarity, common_features
