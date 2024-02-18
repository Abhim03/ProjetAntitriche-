import ast


class CodeASTComparator(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.features = set()
        self.depth = 0  # Initial depth

    def generic_visit(self, node):
        """Increase depth for deeper nodes."""
        self.depth += 1
        super().generic_visit(node)
        self.depth -= 1

    def add_feature(self, node, feature_name):
        """Helper to add features with depth."""
        self.features.add((feature_name, node.lineno, node.col_offset, self.depth))

    def visit_FunctionDef(self, node):
        self.add_feature(node, "FunctionDef")
        self.generic_visit(node)

    def visit_Return(self, node):
        self.add_feature(node, "Return")
        self.generic_visit(node)

    def visit_BinOp(self, node):
        op_type = type(node.op).__name__
        self.add_feature(node, "BinOp-" + op_type)
        self.generic_visit(node)

    def visit_If(self, node):
        self.add_feature(node, "If")
        self.generic_visit(node)

    def visit_For(self, node):
        self.add_feature(node, "For")
        self.generic_visit(node)

    def visit_While(self, node):
        self.add_feature(node, "While")
        self.generic_visit(node)

    def visit_Try(self, node):
        self.add_feature(node, "Try")
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.add_feature(node, f"Call-{node.func.id}")
        elif isinstance(node.func, ast.Attribute):
            self.add_feature(node, f"MethodCall-{node.func.attr}")
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        self.add_feature(node, "Except")
        self.generic_visit(node)

    def visit_Assign(self, node):
        self.add_feature(node, "Assign")
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        op_type = type(node.op).__name__
        self.add_feature(node, f"BoolOp-{op_type}")
        self.generic_visit(node)

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

        return {"percentage": similarity, "common_features": list(common_features)}
