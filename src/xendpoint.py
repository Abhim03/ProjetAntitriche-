from flask import Flask
from flask_restx import Api, Resource, fields, reqparse
from src.code_comparator import compare_codes
from src.firestore_db import FirestoreDB

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="API de Comparaison de Code",
    description="Une API pour comparer le code des candidats avec des solutions de référence.",
)

ns = api.namespace("comparison", description="Opérations de comparaison")

firestore_db = FirestoreDB()

# Modèle de requête pour la soumission de code
code_submission_model = api.model(
    "CodeSubmission",
    {
        "question_id": fields.String(required=True, description="L'ID unique de la question"),
        "candidate_code": fields.String(
            required=True, description="Le code soumis par le candidat"
        ),
    },
)


parser = reqparse.RequestParser()
parser.add_argument(
    "question_id", required=True, help="L'ID unique de la question ne peut être vide."
)
parser.add_argument(
    "candidate_code", required=True, help="Le code soumis par le candidat ne peut être vide."
)


@ns.route("/submit")
class CodeComparison(Resource):
    @api.doc("submit_code")
    @api.expect(parser)
    def post(self):
        args = parser.parse_args()
        question_id = args["question_id"]
        candidate_code = args["candidate_code"]

        question = firestore_db.get_question_by_id(question_id)
        if not question:
            api.abort(404, "La question spécifiée n'a pas été trouvée.")

        code_gpt = question["IA"]
        code_leetcode = question["H"]

        similarity_gpt = compare_codes(candidate_code, code_gpt)
        similarity_leetcode = compare_codes(candidate_code, code_leetcode)

        return {
            "similarity_with_gpt": similarity_gpt["percentage"],
            "similarity_with_leetcode": similarity_leetcode["percentage"],
        }, 200


if __name__ == "__main__":
    app.run(debug=True)
