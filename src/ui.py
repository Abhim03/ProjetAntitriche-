from collections import defaultdict
from analyse_ast import compare_codes
from flask import Flask, render_template, request


def highlight(text, degree):
    max_degree = 5  # arbitrary value

    # scale factor = 255 at degree 0, down to 0 at max_degree
    scale_factor = max(0, min(255 * (1 - (degree / max_degree)), 255))

    return f'<span style="background-color: rgb(255, {scale_factor}, {scale_factor})">{text}</span>'


app = Flask(__name__, template_folder="../templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    code1 = request.form["code1"]
    code2 = request.form["code2"]

    similarity, features = compare_codes(code1, code2)

    # Extracting code snippets for display
    code1_lines = code1.split("\n")
    code2_lines = code2.split("\n")

    line_occurrences = defaultdict(int)
    for feature in features:
        line = feature.line
        line_occurrences[line] += 1

    # Highlight similar parts in code snippets
    for feature in features:
        line = feature.line
        degree = line_occurrences[line]
        if 0 < line <= len(code1_lines) and 0 < line <= len(code2_lines):
            code1_lines[line - 1] = highlight(code1_lines[line - 1], degree)
            code2_lines[line - 1] = highlight(code2_lines[line - 1], degree)

    # Join the modified code lines back together
    highlighted_code1 = "\n".join(code1_lines)
    highlighted_code2 = "\n".join(code2_lines)

    return render_template(
        "index.html",
        similarity_percentage=f"{similarity:.2%}",  # Format similarity as xx.xx%
        highlighted_code1=highlighted_code1,
        highlighted_code2=highlighted_code2,
    )


if __name__ == "__main__":
    app.run(debug=True)
