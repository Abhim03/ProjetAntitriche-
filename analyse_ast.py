# Analyse Comparative Avancée de la Structure du Code en Python

import ast
from flask import Flask, render_template, request


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
        Enhanced to record the position of FunctionDef nodes.
        """
        self.features.append(("FunctionDef", node.lineno, node.col_offset))
        self.generic_visit(node)

    def visit_Return(self, node):
        """
        Enhanced to record the position of Return nodes.
        """
        self.features.append(("Return", node.lineno, node.col_offset))
        self.generic_visit(node)

    def visit_BinOp(self, node):
        """
        Enhanced to record the position of BinOp nodes.
        """
        op_type = type(node.op).__name__
        self.features.append(("BinOp", op_type, node.lineno, node.col_offset))
        self.generic_visit(node)

    def visit_For(self, node):
        """
        Enhanced to record the position of For loops.
        """
        self.features.append(("For", node.lineno, node.col_offset))
        self.generic_visit(node)

    def visit_While(self, node):
        """
        Enhanced to record the position of While loops.
        """
        self.features.append(("While", node.lineno, node.col_offset))
        self.generic_visit(node)

    def visit_Assign(self, node):
        """
        Enhanced to record the position of variable assignments.
        """
        self.features.append(("Assign", node.lineno, node.col_offset))
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        """
        Enhanced to record the position of annotated variable declarations.
        """
        self.features.append(("AnnAssign", node.lineno, node.col_offset))
        self.generic_visit(node)

    def visit_Num(self, node):
        """
        Visite les nœuds Num (nombres) et enregistre la présence d'un nombre.
        """
        self.features.append("Num")
        self.generic_visit(node)

    def compare_codes(self, code1, code2):
        """
        Enhanced to return both similarity percentage and positions of common features.
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
        Enhanced to record the position of FunctionDef nodes including line and column.
        """
        self.features.append(("FunctionDef", node.lineno, node.col_offset))
        self.generic_visit(node)

    def visit_Print(self, node):
        """
        Visite les nœuds Print (instructions d'impression) et compte le nombre d'éléments imprimés.
        """
        self.features.append(("Print", len(node.values)))
        self.generic_visit(node)

    def compare_codes(self, code1, code2):
        """
        Enhanced to return both similarity percentage and detailed matching features.
        """
        tree1 = ast.parse(code1)
        tree2 = ast.parse(code2)

        self.features = []
        self.visit(tree1)
        features1 = {f"{feature}_{i}": feature for i, feature in enumerate(self.features)}

        self.features = []
        self.visit(tree2)
        features2 = {f"{feature}_{i}": feature for i, feature in enumerate(self.features)}

        common_features = set(features1.values()).intersection(set(features2.values()))
        total_features = set(features1.values()).union(set(features2.values()))
        similarity = len(common_features) / len(total_features) if total_features else 0

        detailed_similarity = {"similarity_percentage": similarity, "common_features": list(common_features)}
        return detailed_similarity


# Test des fonctions
comparator = AdvancedCodeComparator()
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    code1 = request.form["code1"]
    code2 = request.form["code2"]
    comparison_result = comparator.compare_codes(code1, code2)

    # Extracting similarity percentage
    similarity_percentage = comparison_result.get("similarity_percentage", 0)

    # Extracting common features along with their positions
    common_features = comparison_result.get("common_features", [])

    # Extracting code snippets for display
    code1_lines = code1.split("\n")
    code2_lines = code2.split("\n")

    # Highlight similar parts in code snippets
    for feature in common_features:
        feature_type, line, col = feature
        # Ensure line is a valid integer
        if isinstance(line, int) and 0 < line <= len(code1_lines) and 0 < line <= len(code2_lines):
            code1_lines[line - 1] = f'<span style="background-color: red">{code1_lines[line - 1]}</span>'
            code2_lines[line - 1] = f'<span style="background-color: red">{code2_lines[line - 1]}</span>'

    # Join the modified code lines back together
    highlighted_code1 = "\n".join(code1_lines)
    highlighted_code2 = "\n".join(code2_lines)

    return render_template(
        "index.html",
        similarity_percentage=f"{similarity_percentage:.2%}",  # Format similarity as xx.xx%
        highlighted_code1=highlighted_code1,
        highlighted_code2=highlighted_code2,
    )


if __name__ == "__main__":
    app.run(debug=True)
