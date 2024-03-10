from flask import Flask, request
from flask_restx import Api, Resource, reqparse, fields
from prompt import generate_response

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="API de Génération de Contenu",
    description="Une API pour générer des réponses à des questions en utilisant OpenAI.",
)

ns = api.namespace("content_generation", description="Opérations de génération de contenu")

content_generation_model = api.model(
    "ContentGeneration",
    {
        "question": fields.String(required=True, description="La question à poser à l'API"),
    },
)

parser = reqparse.RequestParser()
parser.add_argument(
    "question",
    required=True,
    help="La question ne peut être vide.",
    location="json",
)


@ns.route("/generate")
class ContentGeneration(Resource):
    @api.doc("generate_content")
    @api.expect(content_generation_model)
    def post(self):
        args = parser.parse_args()
        question = args["question"]
        response_text = generate_response(question)
        return {"response": response_text}, 200


if __name__ == "__main__":
    app.run(debug=True)
