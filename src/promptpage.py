from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields

from seniorprompt import generate_senior_response
from juniorprompt import generate_junior_response

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="API de Génération de Contenu",
    description="Une API pour générer des réponses à des questions en utilisant un llm local (Mistral), adaptées aux niveaux junior et senior.",
)

ns = api.namespace("content_generation", description="Opérations de génération de contenu")

content_generation_model = api.model(
    "ContentGeneration",
    {
        "level": fields.String(
            required=True,
            description="Le niveau de compétence (junior ou senior)",
        ),
        "question": fields.String(required=True, description="La question à poser à l'API"),
    },
)


@ns.route("/generate")
class ContentGeneration(Resource):
    @api.doc("generate_content")
    @api.expect(content_generation_model)
    def post(self):
        data = request.json
        level = data.get("level")
        question = data.get("question")

        if not question or not level:
            return {"error": "La requête doit contenir à la fois 'level' et 'question'."}, 400

        if level.lower() == "senior":
            response_text = generate_senior_response(question)
        elif level.lower() == "junior":
            response_text = generate_junior_response(question)
        else:
            return {"error": "Le niveau spécifié doit être 'junior' ou 'senior'."}, 400

        return {"response": response_text}, 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
