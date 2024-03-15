import ast
import re


class CodeASTComparator(ast.NodeVisitor):
    @staticmethod
    def normalize_code(code):
        # Supprime les commentaires, normalise les espaces, etc.
        code = re.sub(r"#.*", "", code)  # Supprime les commentaires
        return code

    def __init__(self):
        super().__init__()
        self.features = set()
        self.depth = 0  # Initial depth

    def generic_visit(self, node):
        """Increase depth for deeper nodes."""
        self.depth += 1
        super().generic_visit(node)
        self.depth -= 1

    def add_feature(self, node, feature_name, additional_info=None):
        """Helper to add features with depth and additional info."""
        feature = (feature_name, node.lineno, node.col_offset, self.depth, additional_info)
        self.features.add(feature)

    def visit_FunctionDef(self, node):
        num_params = len(node.args.args)  # Number of parameters
        self.add_feature(node, "FunctionDef", additional_info=f"params:{num_params}")
        self.generic_visit(node)

    def visit_Return(self, node):
        self.add_feature(node, "Return")
        self.generic_visit(node)

    def visit_BinOp(self, node):
        op_type = type(node.op).__name__
        self.add_feature(node, "BinOp", additional_info=op_type)
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
        num_args = len(node.args)  # Number of arguments
        if isinstance(node.func, ast.Name):
            self.add_feature(node, "Call", additional_info=f"{node.func.id}_args:{num_args}")
        elif isinstance(node.func, ast.Attribute):
            self.add_feature(
                node, "MethodCall", additional_info=f"{node.func.attr}_args:{num_args}"
            )
        self.generic_visit(node)

    def visit_Assign(self, node):
        self.add_feature(node, "Assign")
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        op_type = type(node.op).__name__
        self.add_feature(node, "BoolOp", additional_info=op_type)
        self.generic_visit(node)

    def compare_codes(self, code1, code2):
        code1 = CodeASTComparator.normalize_code(code1)
        code2 = CodeASTComparator.normalize_code(code2)

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


def test():
    comparator = CodeASTComparator()
    code1 = """
def add(a,b):
    result = a + b
    return result
"""
    code2 = """
def somme(x,y):
    return x + y
"""
    similarity = comparator.compare_codes(code1, code2)
    print(f"Similarity between code1 and code2: {similarity}")


if __name__ == "__main__":
    test()
