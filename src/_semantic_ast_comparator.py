from transformers import RobertaTokenizer, RobertaModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class SemanticASTComparator:
    def __init__(self):
        self.tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
        self.model = RobertaModel.from_pretrained("microsoft/codebert-base")

    def calculate_semantic_similarity(self, code1, code2):
        embedding1 = self.get_code_embedding(code1)
        embedding2 = self.get_code_embedding(code2)
        similarity = cosine_similarity([embedding1], [embedding2])[0][0]
        return {"percentage": similarity}

    def get_code_embedding(self, code):
        tokens = self.tokenizer(code, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model(**tokens)
        # mean-max pooling
        embeddings = outputs.last_hidden_state
        mean_pooling = torch.mean(embeddings, 1)
        max_pooling, _ = torch.max(embeddings, 1)
        mean_max_pooling = torch.cat((mean_pooling, max_pooling), 1)
        code_embedding = mean_max_pooling.detach().numpy()[0]
        # Normalisation de l'embedding
        return code_embedding / np.linalg.norm(code_embedding)
