from flask import Flask, render_template, request
from AdvancedCodeComparator import AdvancedCodeComparator


comparator = AdvancedCodeComparator()
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    code1 = request.form["code1"]
    code2 = request.form["code2"]
    comparison_result = comparator.compare_codes(code1, code2)

    # Extracting similarity percentage
    similarity_percentage = comparison_result.get("similarity_percentage", 0)

    # Extracting common features along with their positions
    common_features = comparison_result.get("common_features", [])

    # Extracting code snippets for display
    code1_lines = code1.split("\n")
    code2_lines = code2.split("\n")

    # Highlight similar parts in code snippets
    for feature in common_features:
        feature_type, line, col = feature
        # Ensure line is a valid integer
        if isinstance(line, int) and 0 < line <= len(code1_lines) and 0 < line <= len(code2_lines):
            code1_lines[line - 1] = f'<span style="background-color: red">{code1_lines[line - 1]}</span>'
            code2_lines[line - 1] = f'<span style="background-color: red">{code2_lines[line - 1]}</span>'

    # Join the modified code lines back together
    highlighted_code1 = "\n".join(code1_lines)
    highlighted_code2 = "\n".join(code2_lines)

    return render_template(
        "index.html",
        similarity_percentage=f"{similarity_percentage:.2%}",  # Format similarity as xx.xx%
        highlighted_code1=highlighted_code1,
        highlighted_code2=highlighted_code2,
    )


if __name__ == "__main__":
    app.run(debug=True)
