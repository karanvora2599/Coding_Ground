import streamlit as st
import os
import json

def load_questions():
    """
    Load questions from JSON files located in the 'questions' directory.
    """
    # Get the path to the 'questions' directory relative to this file
    questions_dir = os.path.join(os.path.dirname(__file__), 'questions')
    questions = []
    for filename in os.listdir(questions_dir):
        if filename.endswith('.json'):
            with open(os.path.join(questions_dir, filename), 'r') as f:
                question = json.load(f)
                questions.append(question)
    return sorted(questions, key=lambda x: x['id'])

def get_selected_question(selected_question_id, questions):
    """
    Retrieve the selected question based on its ID.
    """
    for q in questions:
        if q['id'] == selected_question_id:
            return q
    return None

def display_question_overlay(questions):
    """
    Display the question overlay, including difficulty and question selection.
    """
    # Initialize session state for selected difficulty
    if 'selected_difficulty' not in st.session_state:
        st.session_state.selected_difficulty = 'Easy'  # Default difficulty

    def difficulty_changed():
        # When difficulty changes, reset the selected question ID
        filtered_questions = [q for q in questions if q['difficulty'] == st.session_state.selected_difficulty]
        if filtered_questions:
            st.session_state.selected_question_id = filtered_questions[0]['id']
        else:
            st.session_state.selected_question_id = None

    # Initialize session state for selected question ID
    if 'selected_question_id' not in st.session_state:
        # Filter questions based on the initial difficulty
        filtered_questions = [q for q in questions if q['difficulty'] == st.session_state.selected_difficulty]
        st.session_state.selected_question_id = filtered_questions[0]['id'] if filtered_questions else None

    # Use a checkbox to toggle the overlay
    st.sidebar.checkbox("Show Question", key='show_question')

    # Difficulty levels
    difficulty_levels = ['Easy', 'Medium', 'Hard']

    # Select difficulty level with callback
    st.sidebar.selectbox(
        "Select Difficulty",
        difficulty_levels,
        index=difficulty_levels.index(st.session_state.selected_difficulty),
        key='selected_difficulty',
        on_change=difficulty_changed
    )

    # Filter questions based on selected difficulty
    filtered_questions = [q for q in questions if q['difficulty'] == st.session_state.selected_difficulty]

    # Select a question from filtered_questions
    if filtered_questions:
        # Map titles to question IDs
        title_to_id = {f"{q['id']}. {q['title']}": q['id'] for q in filtered_questions}
        question_titles = list(title_to_id.keys())
        # Determine selected index
        if st.session_state.selected_question_id in [q['id'] for q in filtered_questions]:
            selected_index = next((i for i, q in enumerate(filtered_questions) if q['id'] == st.session_state.selected_question_id), 0)
        else:
            selected_index = 0
            st.session_state.selected_question_id = filtered_questions[0]['id']
        selected_question_title = st.sidebar.selectbox("Select Question", question_titles, index=selected_index)
        st.session_state.selected_question_id = title_to_id[selected_question_title]
        st.session_state.selected_question_title = selected_question_title
    else:
        st.sidebar.write("No questions available for the selected difficulty.")
        st.session_state.selected_question_id = None

def display_question(selected_question):
    """
    Display the selected question using Streamlit's markdown functions.
    """
    if selected_question:
        st.markdown(f"### {selected_question['id']}. {selected_question['title']}")
        st.markdown(f"**Difficulty:** {selected_question['difficulty']}")
        st.markdown(selected_question['description'])
        st.markdown("#### Examples:")
        for ex in selected_question['examples']:
            st.markdown(f"**Input:** {ex['input']}")
            st.markdown(f"**Output:** {ex['output']}")
            if 'explanation' in ex:
                st.markdown(f"**Explanation:** {ex['explanation']}")
        st.markdown("#### Constraints:")
        for constraint in selected_question['constraints']:
            st.markdown(f"- {constraint}")
    else:
        st.error("Selected question not found.")