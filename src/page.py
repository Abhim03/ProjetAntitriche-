import streamlit as st
from streamlit_ace import st_ace

from src.comparator import compare_codes
from src.firestore_db import FirestoreDB

# Initialize FirestoreDB
firestore_db = FirestoreDB()


def _annotate_code(code: str, similarities: dict):
    """wraps code in html with styling"""
    annotated_code = "<pre style='font-family: monospace; white-space: pre-wrap;'>"
    lines = code.split("\n")
    for i, line in enumerate(lines):
        is_highlighted = False
        for _, lineno, _, _ in similarities["common_features"]:
            if i == lineno - 1:  # Adjusting line number for zero-based index
                annotated_code += f"<mark style='background-color: red;'>{line}</mark>\n"
                is_highlighted = True
                break
        if not is_highlighted:
            annotated_code += line + "\n"
    annotated_code += "</pre>"
    return annotated_code


def run():
    st.title("Plagiarism Detector")
    st.sidebar.title("Settings")
    language = st.sidebar.selectbox("Select a language", ["Python", "C++"])
    columns = st.columns(2)

    if "prefilled_code" not in st.session_state:
        st.session_state.prefilled_code = ""
    if "question_id" not in st.session_state:
        st.session_state.question_id = None

    if st.sidebar.button("Get New Question"):
        new_question = firestore_db.get_random_question(language)
        if new_question:
            st.session_state.question = new_question
            st.sidebar.write(f"Question: {new_question['question']}")
            st.session_state.prefilled_code = new_question.get("prefill", "# Write your code here")
            st.session_state.question_id = new_question["id"]
        else:
            st.sidebar.write("No questions available for this language.")

    # dynamically change the key of the code editor widget, so that it resets for each new question
    editor_key = (
        f"code_editor_{st.session_state.question_id}"
        if st.session_state.question_id
        else "code_editor"
    )

    code = st_ace(
        language="python",
        theme="dracula",
        key=editor_key,
        value=st.session_state.prefilled_code,
    )

    # Submit button for code
    if st.button("Submit Code"):
        if "question" in st.session_state:
            st.write("Code submitted!")
            code_ai = st.session_state.question["IA"]
            code_h = st.session_state.question["H"]

            similarity_ai = compare_codes(code, code_ai)
            similarity_h = compare_codes(code, code_h)

            annotated_code = _annotate_code(code, similarity_ai)
            annotated_code_ai = _annotate_code(code_ai, similarity_ai)

            with columns[0]:
                st.header("Your code")
                st.markdown(annotated_code, unsafe_allow_html=True)
            with columns[1]:
                st.header("AI code")
                st.markdown(annotated_code_ai, unsafe_allow_html=True)

            st.write(f'Similarity with AI code: {similarity_ai["percentage"]}')
            st.write(f'Similarity with Leetcode response code: {similarity_h["percentage"]}')

            seuil = 0.7
            if similarity_ai["percentage"] > seuil:
                st.write("This code is likely written by AI.")
            elif similarity_h["percentage"] > seuil:
                st.write("This code is likely plagiarized from a coding website.")
            else:
                st.write("There is likely no plagiarism.")

            # Fetch a new question for the next run
            st.session_state.question = firestore_db.get_random_question(language)
        else:
            st.write("Please get a new question first.")
