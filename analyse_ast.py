# Analyse Comparative Avancée de la Structure du Code en Python


import ast


class StructuralCodeComparator(ast.NodeVisitor):
    """
    Classe pour comparer la structure de base de deux segments de code Python.
    Elle utilise l'analyse d'AST pour extraire des caractéristiques structurelles clés telles que
    les définitions de fonctions,
    les opérations binaires, et les instructions de retour, et les compare pour calculer un taux de similarité.
    """

    def __init__(self):
        """
        Initialise la liste des caractéristiques extraites du code.
        """
        self.features = []

    def visit_FunctionDef(self, node):
        """
        Visite les nœuds FunctionDef (définition de fonction) et enregistre la présence d'une définition de fonction.
        """
        self.features.append("FunctionDef")
        self.generic_visit(node)

    def visit_Return(self, node):
        """
        Visite les nœuds Return (instruction de retour) et enregistre la présence d'une instruction de retour.
        """
        self.features.append("Return")
        self.generic_visit(node)

    def visit_BinOp(self, node):
        """
        Visite les nœuds BinOp (opérations binaires) et enregistre le type d'opération binaire effectuée.
        """
        op_type = type(node.op).__name__
        self.features.append(("BinOp", op_type))
        self.generic_visit(node)

    def visit_Num(self, node):
        """
        Visite les nœuds Num (nombres) et enregistre la présence d'un nombre.
        """
        self.features.append("Num")
        self.generic_visit(node)

    def compare_codes(self, code1, code2):
        """
        Compare deux morceaux de code en analysant leur structure AST et
        en calculant la similarité basée sur les caractéristiques extraites.

        Args:
            code1 (str): Premier segment de code à comparer.
            code2 (str): Second segment de code à comparer.

        Returns:
            float: Taux de similarité entre les deux segments de code.
        """
        tree1 = ast.parse(code1)
        tree2 = ast.parse(code2)

        self.features = []
        self.visit(tree1)
        features1 = frozenset(self.features)

        self.features = []
        self.visit(tree2)
        features2 = frozenset(self.features)

        common_features = features1.intersection(features2)
        total_features = features1.union(features2)
        similarity = len(common_features) / len(total_features) if total_features else 0
        return similarity


class AdvancedCodeComparator(StructuralCodeComparator):
    """
    Classe avancée pour comparer la structure de code Python. Elle étend StructuralCodeComparator en ajoutant
    la prise en compte de la longueur du corps des fonctions et le nombre d'éléments imprimés, fournissant ainsi
    une analyse plus fine de la structure du code.
    """

    def visit_FunctionDef(self, node):
        """
        Visite les nœuds FunctionDef et enregistre la longueur du corps de la fonction.
        """
        self.features.append(("FunctionDef", len(node.body)))
        self.generic_visit(node)

    def visit_Print(self, node):
        """
        Visite les nœuds Print (instructions d'impression) et compte le nombre d'éléments imprimés.
        """
        self.features.append(("Print", len(node.values)))
        self.generic_visit(node)

    # Vous pouvez étendre cette classe avec d'autres méthodes pour couvrir plus d'éléments de la structure du code.


# Test des fonctions
comparator = AdvancedCodeComparator()
code1 = "def somme(a, b): print(a + b)"
code2 = "def ajout(a,b): return(a+b)"

similarity = comparator.compare_codes(code1, code2)
print(f"Taux de similarité : {similarity * 100:.2f}%")
