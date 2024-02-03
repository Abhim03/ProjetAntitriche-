from transformers import RobertaTokenizer, RobertaModel
from sklearn.metrics.pairwise import cosine_similarity


class SemanticASTComparator:
    def __init__(self):
        self.tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
        self.model = RobertaModel.from_pretrained("microsoft/codebert-base")

    def calculate_semantic_similarity(self, code1, code2):
        embedding1 = self.get_code_embedding(code1)
        embedding2 = self.get_code_embedding(code2)
        similarity = cosine_similarity([embedding1], [embedding2])[0, 0]

        return {"percentage": similarity}

    def get_code_embedding(self, code):
        tokens = self.tokenizer(code, return_tensors="pt")
        output = self.model(**tokens)
        return output.last_hidden_state.mean(dim=1).detach().numpy()
