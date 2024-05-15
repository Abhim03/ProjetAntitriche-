from flask import Flask, render_template, request
from _code_ast_comparator import CodeASTComparator

app = Flask(__name__)
code_comparator = CodeASTComparator()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    code1 = request.form["code1"]
    code2 = request.form["code2"]
    comparison_result = code_comparator.compare_codes(code1, code2)
    similarity_percentage = comparison_result["percentage"]
    common_features = comparison_result["common_features"]
    highlighted_code1, highlighted_code2 = code_comparator.highlight_code(
        code1,
        code2,
        common_features,
    )

    return render_template(
        "index.html",
        similarity_percentage=f"{similarity_percentage*100:.2f}%",
        highlighted_code1=highlighted_code1,
        highlighted_code2=highlighted_code2,
        common_features=common_features,
    )


if __name__ == "__main__":
    app.run(debug=True)
