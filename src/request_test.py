import requests
import json

url = "https://21f7-129-104-252-51.ngrok-free.app/comparaison/submit"
data = {
    "question_id": "somme",
    "candidate_code": "def add(a, b):\n    return a + b\n",
}
response = requests.post(url, json=data)
print(response)
pretty_response = json.dumps(response.json(), indent=2)
print(pretty_response)
SUCCESS = 200
assert response.status_code == SUCCESS
