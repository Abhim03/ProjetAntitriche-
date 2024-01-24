import ast


class _CodeComparator(ast.NodeVisitor):
    def __init__(self):
        self.features = set()

    def visit_FunctionDef(self, node):
        # Record the position of FunctionDef nodes.

        self.features.add(("FunctionDef", node.lineno, node.col_offset, None))
        self.generic_visit(node)

    def visit_Return(self, node):
        # Record the position of Return nodes.

        self.features.add(("Return", node.lineno, node.col_offset, None))
        self.generic_visit(node)

    def visit_BinOp(self, node):
        # Record the position of BinOp nodes.

        op_type = type(node.op).__name__
        self.features.add(("BinOp", node.lineno, node.col_offset, op_type))
        self.generic_visit(node)

    def visit_For(self, node):
        # Record the position of For loops.

        self.features.add(("For", node.lineno, node.col_offset, None))
        self.generic_visit(node)

    def visit_Print(self, node):
        """
        Visite les nœuds Print et compte le nombre d'éléments imprimés.
        """
        self.features.add(("Print", node.lineno, node.col_offset, len(node.values)))
        self.generic_visit(node)


def compare_codes(code1, code2):
    """
    Return both similarity percentage and detailed matching features.
    """
    comparator1 = _CodeComparator()
    comparator2 = _CodeComparator()

    tree1 = ast.parse(code1)
    tree2 = ast.parse(code2)

    comparator1.visit(tree1)
    comparator2.visit(tree2)

    common_features = comparator1.features.intersection(comparator2.features)
    total_features = comparator1.features.union(comparator2.features)

    similarity = len(common_features) / len(total_features) if total_features else 0

    return {"percentage": similarity, "common_features": common_features}
