import requests
import json


def generate_senior_response(question):
    url = "https://af75-129-104-252-51.ngrok-free.app/v1/completions"  # Ajusté pour l'endpoint de chat  # noqa: E501
    headers = {
        "Authorization": "Bearer votre_clé_api",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-3.5-turbo",  # Ajustez au modèle disponible pour chat completions
        "messages": [
            {
                "role": "system",
                "content": "Vous êtes un programmeur senior très expérimenté. Votre code est clair, bien organisé, et gère correctement les erreurs.",  # noqa: E501
            },
            {"role": "user", "content": f"{question}"},
        ],
        "temperature": 0.0,
        "max_tokens": 150,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:  # noqa: PLR2004
        return response.json()["choices"][0]["message"]["content"].strip()
    else:  # noqa: RET505
        return f"Erreur: {response.status_code} - {response.text}"
