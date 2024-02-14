from transformers import pipeline


class CodeGenerator:
    def __init__(self, model_name="gpt2"):
        self.generator = pipeline("text-generation", model=model_name)

    def generate_code(self, prompt, max_length=100):
        # Génère du texte basé sur le prompt fourni
        generated_texts = self.generator(prompt, max_length=max_length, num_return_sequences=1)

        if isinstance(generated_texts, list) and len(generated_texts) > 0:
            return generated_texts[0].get("generated_text", "")
        else:
            return "Aucun texte généré"
