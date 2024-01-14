import ast
from .StructuralCodeComparator import StructuralCodeComparator


class AdvancedCodeComparator(StructuralCodeComparator):
    """
    Classe avancée pour comparer la structure de code Python. Elle étend StructuralCodeComparator en ajoutant
    la prise en compte de la longueur du corps des fonctions et le nombre d'éléments imprimés, fournissant ainsi
    une analyse plus fine de la structure du code.
    """

    def visit_FunctionDef(self, node):
        """
        Enhanced to record the position of FunctionDef nodes including line and column.
        """
        self.features.add(("FunctionDef", node.lineno, node.col_offset))
        self.generic_visit(node)

    def visit_Print(self, node):
        """
        Visite les nœuds Print (instructions d'impression) et compte le nombre d'éléments imprimés.
        """
        self.features.add(("Print", len(node.values)))
        self.generic_visit(node)

    def compare_codes(self, code1, code2):
        """
        Enhanced to return both similarity percentage and detailed matching features.
        """
        tree1 = ast.parse(code1)
        tree2 = ast.parse(code2)

        self.features = set()
        self.visit(tree1)
        features1 = {f"{feature}_{i}": feature for i, feature in enumerate(self.features)}

        self.features = set()
        self.visit(tree2)
        features2 = {f"{feature}_{i}": feature for i, feature in enumerate(self.features)}

        common_features = set(features1.values()).intersection(set(features2.values()))
        total_features = set(features1.values()).union(set(features2.values()))
        similarity = len(common_features) / len(total_features) if total_features else 0

        detailed_similarity = {"similarity_percentage": similarity, "common_features": list(common_features)}
        return detailed_similarity
