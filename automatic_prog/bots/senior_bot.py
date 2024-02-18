from utils.code_generation_utils import CodeGenerator


class SeniorBot:
    def __init__(self):
        self.code_generator = CodeGenerator(model_name="gpt2-medium")

    def generate_code(self, problem_description):
        prompt = f"Senior Level: Écris une fonction avancée et bien documentée en Python pour : {problem_description}. Assure-toi d'inclure la gestion des erreurs."
        return self.code_generator.generate_code(prompt, max_length=200)
