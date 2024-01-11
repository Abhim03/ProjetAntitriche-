from analyse_ast import compare_codes
from firestore_db import FirestoreDB
from flask import Flask, jsonify, request

app = Flask(__name__)
db = FirestoreDB()


@app.route("/compare_code", methods=["POST"])
def compare_code():
    data = request.get_json()
    question_id = data.get("question_id", "")
    candidate_code = data.get("candidate_code", "")

    # Récupérer la question depuis la base de données
    question_data = db.get_question(question_id)
    # gpt_code = question_data.get('gpt_code', '')
    # leetcode_code = question_data.get('leetcode_code', '')

    # Comparer le code du candidat avec les codes GPT et LeetCode
    result = compare_codes(candidate_code, candidate_code)
    # result2 = code_comparator.compare_codes(candidate_code, leetcode_code)
    # result = max(result1, result2)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
