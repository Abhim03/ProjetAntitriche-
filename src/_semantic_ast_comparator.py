from transformers import RobertaTokenizer, RobertaModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SemanticASTComparator:
    tokenizer = None
    model = None

    @classmethod
    def initialize_model_and_tokenizer(cls):
        if cls.tokenizer is None or cls.model is None:
            cls.tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
            cls.model = RobertaModel.from_pretrained("microsoft/codebert-base")

    def __init__(self):
        # Assurez-vous que le modèle et le tokenizer sont chargés une seule fois.
        self.initialize_model_and_tokenizer()

    def calculate_semantic_similarity(self, code1, code2):
        try:
            embedding1 = self.get_code_embedding(code1)
            embedding2 = self.get_code_embedding(code2)
            similarity = cosine_similarity([embedding1], [embedding2])[0][0]
            return similarity
        except Exception as e:
            # Gestion robuste des erreurs
            print(f"Error during semantic similarity calculation: {e}")
            return {"percentage": 0.0, "error": str(e)}

    def get_code_embedding(self, code):
        try:
            tokens = self.tokenizer(code, return_tensors="pt", truncation=True, max_length=512)
            outputs = self.model(**tokens)
            embeddings = outputs.last_hidden_state
            mean_pooling = torch.mean(embeddings, 1)
            max_pooling, _ = torch.max(embeddings, 1)
            mean_max_pooling = torch.cat((mean_pooling, max_pooling), 1)
            code_embedding = mean_max_pooling.detach().numpy()[0]
            # Normalisation de l'embedding pour une comparaison plus fiable
            return code_embedding / np.linalg.norm(code_embedding)
        except Exception as e:
            # Gestion robuste des erreurs
            print(f"Error during code embedding generation: {e}")
            return np.zeros(1)  # Retourner un vecteur nul en cas d'erreur

