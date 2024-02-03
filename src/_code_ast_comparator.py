import ast


class CodeASTComparator(ast.NodeVisitor):
    def __init__(self):
        self.features = set()

    def visit_FunctionDef(self, node):
        self.features.add(("FunctionDef", node.lineno, node.col_offset, None))
        self.generic_visit(node)

    def visit_Return(self, node):
        self.features.add(("Return", node.lineno, node.col_offset, None))
        self.generic_visit(node)

    def visit_BinOp(self, node):
        op_type = type(node.op).__name__
        self.features.add(("BinOp", node.lineno, node.col_offset, op_type))
        self.generic_visit(node)

    # Ajoutez d'autres méthodes d'analyse syntaxique si nécessaire

    def compare_codes(self, code1, code2):
        comparator1 = CodeASTComparator()
        comparator2 = CodeASTComparator()

        tree1 = ast.parse(code1)
        tree2 = ast.parse(code2)

        comparator1.visit(tree1)
        comparator2.visit(tree2)

        common_features = comparator1.features.intersection(comparator2.features)
        total_features = comparator1.features.union(comparator2.features)

        similarity = len(common_features) / len(total_features) if total_features else 0

        return {"percentage": similarity, "common_features": common_features}
