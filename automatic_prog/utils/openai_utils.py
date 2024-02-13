# utils/openai_utils.py

import openai


def setup_openai_api(api_key):
    """
    Configure l'API key pour OpenAI.

    """
    openai.api_key = api_key


def generate_openai_response(prompt, engine="code-davinci-002", temperature=0.7, max_tokens=100):
    """
    Génère une réponse de l'API OpenAI basée sur un prompt.

    Args:
        prompt (str): Le prompt à envoyer à l'API.
        engine (str): Le moteur d'IA à utiliser pour la génération de réponse.
        temperature (float): Contrôle la créativité de la réponse.
        max_tokens (int): Le nombre maximum de tokens dans la réponse.

    Returns:
        str: La réponse générée par l'API OpenAI.
    """
    try:
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Erreur lors de la génération de la réponse: {str(e)}"
