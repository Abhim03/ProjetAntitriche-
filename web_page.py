import streamlit as st
from streamlit_ace import st_ace

import random

from src import FirestoreDB
from src.AdvancedCodeComparator import AdvancedCodeComparator
from src.StructuralCodeComparator import StructuralCodeComparator

columns = st.columns(2)
# Initialize FirestoreDB and Comparator
firebase_db = FirestoreDB()
comparator = StructuralCodeComparator()
advanced_comparator = AdvancedCodeComparator()


def annotate_code(code, similarities):
    annotated_code = "<pre style='font-family: monospace; white-space: pre-wrap;'>"
    lines = code.split("\n")
    for i, line in enumerate(lines):
        is_highlighted = False
        for feature, lineno, col_offset in similarities["common_features"]:
            if i == lineno - 1:  # Adjusting line number for zero-based index
                annotated_code += f"<mark style='background-color: red;'>{line}</mark>\n"
                is_highlighted = True
                break
        if not is_highlighted:
            annotated_code += line + "\n"
    annotated_code += "</pre>"
    return annotated_code


# Function to get a random question for a given language
def get_random_question(language):
    questions = [q for q in firebase_db.get_all_documents("Questions")]
    return random.choice(questions) if questions else None


# Streamlit layout
st.title("Anti-Cheating Code Comparator")

# Sidebar
st.sidebar.title("Settings")

# Language selection
language = st.sidebar.selectbox("Select a language", ["Python", "Java", "C++"])

# Button to get a new question
if st.sidebar.button("Get New Question"):
    st.session_state.question = get_random_question(language)
    if st.session_state.question:
        st.sidebar.write(f"Question: {st.session_state.question['question']}")
    else:
        st.sidebar.write("No questions available for this language.")

# Main area for code submission
code = st_ace(language="python", theme="dracula", key="code_editor")

# Submit button for code
if st.button("Submit Code"):
    if "question" in st.session_state:
        st.write("Code submitted!")

        code_Ai = st.session_state.question["IA"]
        code_H = st.session_state.question["H"]

        similarity_AI = comparator.compare_codes(code, code_Ai)
        similarity_H = comparator.compare_codes(code, code_H)

        advanced_similarity_AI = advanced_comparator.compare_codes(code, code_Ai)
        advanced_similarity_H = advanced_comparator.compare_codes(code, code_H)

        annotated_code = annotate_code(code, advanced_similarity_AI)
        annotated_code_AI = annotate_code(code_Ai, advanced_similarity_AI)
        with columns[0]:
            st.header("Your code")
            st.markdown(annotated_code, unsafe_allow_html=True)
        with columns[1]:
            st.header("AI code")
            st.markdown(annotated_code_AI, unsafe_allow_html=True)
        st.write(f"Similarity with AI code: {similarity_AI}")
        st.write(f"Similarity with Human code: {similarity_H}")

        if similarity_AI > similarity_H:
            st.write("This code is likely written by AI.")
        else:
            st.write("This code is likely written by Human.")

        # Fetch a new question for the next run
        st.session_state.question = get_random_question(language)
    else:
        st.write("Please select a question first.")
