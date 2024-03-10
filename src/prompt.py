import openai

openai.api_key = "votre_clé_api"


def generate_response(question):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # ou une version plus récente si disponible
            prompt=question,
            temperature=0.7,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)
