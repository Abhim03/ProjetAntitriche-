import streamlit as st
from streamlit_ace import st_ace

import random

from src import FirestoreDB
from src.code_comparator import compare_codes

columns = st.columns(2)
# Initialize FirestoreDB and Comparator
firebase_db = FirestoreDB()


def annotate_code(code, similarities):
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


# Function to get a random question for a given language
def get_random_question(language):  # noqa: ARG001
    questions = list(firebase_db.get_all_documents("Questions"))
    return random.choice(questions) if questions else None


# Streamlit layout
st.title("Anti-Cheating Code Comparator")

# Sidebar
st.sidebar.title("Settings")

# Language selection
language = st.sidebar.selectbox("Select a language", ["Python", "C++"])


# Button to get a new question
if st.sidebar.button("Get New Question"):
    st.session_state.question = get_random_question(language)
    if st.session_state.question:
        st.sidebar.write(f"Question: {st.session_state.question['question']}")
    else:
        st.sidebar.write("No questions available for this language.")

# Main area for code submission
code = st_ace(value="class Solution:\n\t", language="python", theme="dracula", key="code_editor")

# Submit button for code
if st.button("Submit Code"):
    if "question" in st.session_state:
        st.write("Code submitted!")
        assert st.session_state.question is not None
        code_ai = st.session_state.question["IA"]
        code_h = st.session_state.question["H"]

        similarity_ai = compare_codes(code, code_ai)
        similarity_h = compare_codes(code, code_h)

        annotated_code = annotate_code(code, similarity_ai)
        annotated_code_ai = annotate_code(code_ai, similarity_ai)
        with columns[0]:
            st.header("Your code")
            st.markdown(annotated_code, unsafe_allow_html=True)
        with columns[1]:
            st.header("AI code")
            st.markdown(annotated_code_ai, unsafe_allow_html=True)
        st.write(f'Similarity with AI code: {similarity_ai["similarity_percentage"]}')
        st.write(f'Similarity with Leetcode response code: {similarity_h["similarity_percentage"]}')
        seuil = 0.7
        if similarity_ai["similarity_percentage"] > seuil:
            st.write("This code is likely written by AI.")
        elif similarity_h["similarity_percentage"] > seuil:
            st.write("This code is likely plagiarized from a coding website.")
        else:
            st.write("There is likely no plagiarism.")

        # Fetch a new question for the next run
        st.session_state.question = get_random_question(language)
    else:
        st.write("Please select a question first.")
