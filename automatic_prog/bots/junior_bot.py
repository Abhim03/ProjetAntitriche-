from utils.code_generation_utils import CodeGenerator


class JuniorBot:
    def __init__(self):
        self.code_generator = CodeGenerator(model_name="gpt2")

    def generate_code(self, problem_description):
        prompt = f"Junior Level: Écris une fonction simple et basique en Python pour : {problem_description}"
        return self.code_generator.generate_code(prompt, max_length=150)
