# Analyse Comparative Avancée de la Structure du Code en Python

from __future__ import annotations

import ast
from ast import NodeVisitor
from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Feature:
    """Classe pour stocker les caractéristiques extraites du code."""

    feature_type: str
    line: int
    column: int
    metadata: str | None


class CodeAST(NodeVisitor):

    """
    Classe pour l'analyse comparative de structures de code Python. Utilise l'analyse d'AST pour comparer des éléments
    clés comme les définitions de fonctions et les opérations binaires. Intègre des métriques supplémentaires comme
    la longueur du corps des fonctions et le nombre d'éléments imprimés pour une évaluation plus précise de la
    similarité.
    """

    def __init__(self):
        """
        Initialise la liste des caractéristiques extraites du code.
        """
        self.features: list[Feature] = []

    def visit_Return(self, node):
        """
        Enhanced to record the position of Return nodes.
        """
        self.features.append(Feature("Return", node.lineno, node.col_offset, None))
        self.generic_visit(node)

    def visit_BinOp(self, node):
        """
        Enhanced to record the position of BinOp nodes.
        """
        op_type = type(node.op).__name__
        self.features.append(Feature("BinOp", node.lineno, node.col_offset, op_type))
        self.generic_visit(node)

    def visit_For(self, node):
        """
        Enhanced to record the position of For loops.
        """
        self.features.append(Feature("For", node.lineno, node.col_offset, None))
        self.generic_visit(node)

    def visit_While(self, node):
        """
        Enhanced to record the position of While loops.
        """
        self.features.append(Feature("While", node.lineno, node.col_offset, None))
        self.generic_visit(node)

    def visit_Assign(self, node):
        """
        Enhanced to record the position of variable assignments.
        """
        self.features.append(Feature("Assign", node.lineno, node.col_offset, None))
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        """
        Enhanced to record the position of annotated variable declarations.
        """
        self.features.append(Feature("AnnAssign", node.lineno, node.col_offset, None))
        self.generic_visit(node)

    def visit_Num(self, node):
        """
        Visite les nœuds Num (nombres) et enregistre la présence d'un nombre.
        """
        self.features.append(Feature("Num", node.lineno, node.col_offset, None))
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        """
        Enhanced to record the position of FunctionDef nodes including line and column.
        """
        self.features.append(Feature("FunctionDef", node.lineno, node.col_offset, None))
        self.generic_visit(node)

    def visit_Print(self, node):
        """
        Visite les nœuds Print (instructions d'impression) et compte le nombre d'éléments imprimés.
        """
        self.features.append(Feature("Print", node.lineno, node.col_offset, node.values))
        self.generic_visit(node)


def compare_codes(code1: str, code2: str):
    """
    Enhanced to return both similarity percentage and detailed matching features.
    """

    code_ast1 = CodeAST()
    code_ast1.visit(ast.parse(code1))

    code_ast2 = CodeAST()
    code_ast2.visit(ast.parse(code2))

    common_features = set(code_ast1.features).intersection(set(code_ast2.features))
    total_features = set(code_ast1.features).union(set(code_ast2.features))

    similarity = len(common_features) / len(total_features) if total_features else 0

    return similarity, common_features
