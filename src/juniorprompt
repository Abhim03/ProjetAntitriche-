import openai


def generate_junior_response(question):
    openai.api_key = "votre_clé_api"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Écris-moi une fonction simple et basique pour : {question}",
        temperature=0.7,
        max_tokens=150,
    )
    return response.choices[0].text.strip()
