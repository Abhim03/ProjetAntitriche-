import ast
import re


class CodeASTComparator(ast.NodeVisitor):
    @staticmethod
    def normalize_code(code):
        # Supprime les commentaires, normalise les espaces, etc.
        return re.sub(r"#.*", "", code)  # Supprime les commentaires

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
                node,
                "MethodCall",
                additional_info=f"{node.func.attr}_args:{num_args}",
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

    def highlight_code(self, code1, code2, common_features):
        code1_lines = code1.split("\n")
        code2_lines = code2.split("\n")

        highlighted_lines1 = {feature[2] for feature in common_features}
        highlighted_lines2 = {feature[2] for feature in common_features}

        for lineno in highlighted_lines1:
            if lineno < len(code1_lines):
                code1_lines[lineno - 1] = (
                    f"<span style='background-color: red'>{code1_lines[lineno - 1]}</span>"
                )

        for lineno in highlighted_lines2:
            if lineno < len(code2_lines):
                code2_lines[lineno - 1] = (
                    f"<span style='background-color: red'>{code2_lines[lineno - 1]}</span>"
                )

        return "\n".join(code1_lines), "\n".join(code2_lines)


def test():
    comparator = CodeASTComparator()
    code1 = """
def contient_pair(nums):
    for num in nums:  # noqa: SIM110
        if num % 2 == 0:
            return True
    return False

liste_nums = [1, 3, 5, 2, 9]
print(contient_pair(liste_nums))
"""
    code2 = """
def has_even(numbers):
    for number in numbers:  # noqa: SIM110
        if number % 2 == 0:
            return True
    return False

test_numbers = [7, 11, 15, 22, 17]
print(has_even(test_numbers))

"""
    similarity = comparator.compare_codes(code1, code2)
    print(f"Similarity between code1 and code2: {similarity}")


if __name__ == "__main__":
    test()
