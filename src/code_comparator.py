import ast


class _CodeComparator(ast.NodeVisitor):
    def __init__(self):
        self.features = set()

    def visit_FunctionDef(self, node):
        # Enhanced to record the position of FunctionDef nodes.

        self.features.add(("FunctionDef", node.lineno, node.col_offset, None))
        self.generic_visit(node)

    def visit_Return(self, node):
        # Enhanced to record the position of Return nodes.

        self.features.add(("Return", node.lineno, node.col_offset, None))
        self.generic_visit(node)

    def visit_BinOp(self, node):
        # Enhanced to record the position of BinOp nodes.

        op_type = type(node.op).__name__
        self.features.add(("BinOp", node.lineno, node.col_offset, op_type))
        self.features.update(self.analyze_expression(node))
        self.generic_visit(node)

    def analyze_expression(self, node):
        """
        Analyse des expressions dans les nœuds BinOp.
        """

        return set()

    def visit_For(self, node):
        # Enhanced to record the position of For loops.

        self.features.add(("For", node.lineno, node.col_offset, None))
        self.features.update(self.analyze_for_loop(node))
        self.generic_visit(node)

    def analyze_for_loop(self, node):
        """Analyse des caractéristiques spécifiques aux boucles For"""

        # Ajoutez ici votre logique d'analyse spécifique aux boucles For
        return set()

    # Ajoutez d'autres méthodes d'analyse pour les différentes caractéristiques que vous souhaitez intégrer

    def visit_Print(self, node):
        """
        Visite les nœuds Print (instructions d'impression) et compte le nombre d'éléments imprimés.
        """
        self.features.add(("Print", len(node.values)))
        self.generic_visit(node)


def compare_codes(code1: str, code2: str):
    """
    Enhanced to return both similarity percentage and detailed matching features.
    """
    comparator1 = _CodeComparator()
    comparator2 = _CodeComparator()

    tree1 = ast.parse(code1)
    tree2 = ast.parse(code2)

    comparator1.visit(tree1)
    features1 = {f"{feature}_{i}": feature for i, feature in enumerate(comparator1.features)}

    comparator2.visit(tree2)
    features2 = {f"{feature}_{i}": feature for i, feature in enumerate(comparator2.features)}

    common_features = set(features1.values()).intersection(set(features2.values()))
    total_features = set(features1.values()).union(set(features2.values()))
    similarity = len(common_features) / len(total_features) if total_features else 0

    return {"similarity_percentage": similarity, "common_features": common_features}
