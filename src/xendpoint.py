from flask import Flask, request, jsonify
from src.code_comparator import compare_codes
from src.firestore_db import FirestoreDB

app = Flask(__name__)

firestore_db = FirestoreDB()


@app.route("/submit_code", methods=["POST"])
def submit_code():
    # Récupérer la question ID et le code du candidat depuis la requête
    data = request.get_json()
    question_id = data.get("question_id")
    candidate_code = data.get("candidate_code")

    question = firestore_db.get_question_by_id(question_id)
    if not question_id or not candidate_code:
        return jsonify({"error": "Missing question_id or candidate_code"}), 400

    code_gpt = question["IA"]
    code_leetcode = question["H"]

    # Calculer les similarités
    similarity_gpt = compare_codes(candidate_code, code_gpt)
    similarity_leetcode = compare_codes(candidate_code, code_leetcode)

    # Construire la réponse
    response = {
        "similarity_with_gpt": similarity_gpt["percentage"],
        "similarity_with_leetcode": similarity_leetcode["percentage"],
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
