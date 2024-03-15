from _code_ast_comparator import CodeASTComparator
from _semantic_ast_comparator import SemanticASTComparator

seuil1 = 0.8
seuil2 = 0.7
seuil3 = 1000


class CodeComparator:
    def __init__(self):
        self.ast_comparator = CodeASTComparator()
        self.semantic_comparator = SemanticASTComparator()

    def compare_codes(self, code1, code2):
        # Ajustement dynamiquement des poids
        syntax_weight, semantic_weight = self.adjust_weights_based_on_length(code1, code2)

        syntax_similarity = self.ast_comparator.compare_codes(code1, code2)

        semantic_similarity = self.semantic_comparator.calculate_semantic_similarity(code1, code2)

        # Vérifier si l'une des similarités dépasse 80%
        if syntax_similarity["percentage"] > seuil1:
            return {
                "percentage": syntax_similarity["percentage"],
                "alert": "High syntax similarity detected. Potential plagiarism.",
            }
        elif semantic_similarity["percentage"] > seuil1:
            return {
                "percentage": semantic_similarity["percentage"],
                "alert": "High semantic similarity detected. Potential plagiarism.",
            }
        else:
            # Calculer la similarité combinée avec des poids dynamiques
            combined_similarity = (
                syntax_weight * syntax_similarity["percentage"]
                + semantic_weight * semantic_similarity["percentage"]
            )

            if combined_similarity > seuil2:
                return {
                    "percentage": combined_similarity,
                    "alert": "Plagiarism likely. Combined similarity exceeds threshold.",
                }
            else:
                return {
                    "percentage": combined_similarity,
                    "alert": "No significant similarity detected.",
                }

    def adjust_weights_based_on_length(self, code1, code2):
        length = max(len(code1), len(code2))
        if length > seuil3:  # Seuil pour un code considéré comme "long"
            return (0.4, 0.6)  # Augmenter le poids de l'analyse sémantique pour les codes longs
        else:
            return (0.5, 0.5)  # Poids égaux pour les codes courts


def test():
    comparator = CodeComparator()
    code1 = "def add(a, b): return a + b"
    code2 = "def add(a, b): return a + b"
    similarity = comparator.compare_codes(code1, code2)
    print(f"Similarity between code1 and code2: {similarity}")


if __name__ == "__main__":
    test()
