import openai


class SeniorBot:
    def __init__(self, openai_api_key):
        self.api_key = openai_api_key
        openai.api_key = self.api_key

    def generate_code(self, problem_description):
        prompt = f"Écris une fonction avancée et bien documentée en Python pour : {problem_description}. Assure-toi d'inclure la gestion des erreurs et des commentaires explicatifs."
        try:
            response = openai.Completion.create(
                engine="code-davinci-002",
                prompt=prompt,
                temperature=0.7,
                max_tokens=150,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return str(e)
