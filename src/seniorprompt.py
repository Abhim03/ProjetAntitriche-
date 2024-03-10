import openai


def generate_senior_response(question):
    openai.api_key = "votre_clé_api"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Écris-moi une fonction claire, très bien organisée, à complexité optimale, avec gestion des erreurs pour : {question}",
        temperature=0.5,
        max_tokens=150,
    )
    return response.choices[0].text.strip()
