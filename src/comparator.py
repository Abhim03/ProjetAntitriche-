from _code_ast_comparator import CodeASTComparator
from _semantic_ast_comparator import SemanticASTComparator


class CodeComparator:
    def __init__(self, syntax_weight=0.5, semantic_weight=0.5):
        self.syntax_weight = syntax_weight
        self.semantic_weight = semantic_weight
        self.ast_comparator = CodeASTComparator()
        self.semantic_comparator = SemanticASTComparator()

    def compare_codes(self, code1, code2):
        # Analyse syntaxique
        syntax_similarity = self.ast_comparator.compare_codes(code1, code2)

        # Analyse sémantique
        semantic_similarity = self.semantic_comparator.calculate_semantic_similarity(code1, code2)

        # Combinaison avec des poids
        combined_similarity = (
            self.syntax_weight * syntax_similarity["percentage"]
            + self.semantic_weight * semantic_similarity["percentage"]
        )

        return {"combined_percentage": combined_similarity}
