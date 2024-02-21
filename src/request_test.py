import requests
import json

url = "http://localhost:5000/comparison/submit"
data = {
    "question_id": "somme",
    "candidate_code": "def add(a, b):\n    return a + b\n",
}
response = requests.post(url, json=data)
pretty_response = json.dumps(response.json(), indent=2)
print(pretty_response)
SUCCESS = 200
assert response.status_code == SUCCESS
