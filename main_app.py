import streamlit as st
from streamlit_ace import st_ace
from executor import execute_code
import html
import options
import os
import json

# Set the page configuration to wide layout
st.set_page_config(layout="wide")

def main():
    st.title("Coding Grounds")

    # Initialize session state variables if not set
    # Font size
    if 'font_size_slider' not in st.session_state:
        st.session_state['font_size_slider'] = 14
    if 'font_size_input' not in st.session_state:
        st.session_state['font_size_input'] = 14

    # Editor height
    if 'editor_height_slider' not in st.session_state:
        st.session_state['editor_height_slider'] = 600
    if 'editor_height_input' not in st.session_state:
        st.session_state['editor_height_input'] = 600

    # Callback functions for synchronization
    def font_size_slider_changed():
        st.session_state.font_size_input = st.session_state.font_size_slider

    def font_size_input_changed():
        st.session_state.font_size_slider = st.session_state.font_size_input

    def editor_height_slider_changed():
        st.session_state.editor_height_input = st.session_state.editor_height_slider

    def editor_height_input_changed():
        st.session_state.editor_height_slider = st.session_state.editor_height_input

    # Load questions from the 'questions' folder
    def load_questions():
        questions_dir = 'questions'
        questions = []
        for filename in os.listdir(questions_dir):
            if filename.endswith('.json'):
                with open(os.path.join(questions_dir, filename), 'r') as f:
                    question = json.load(f)
                    questions.append(question)
        return sorted(questions, key=lambda x: x['id'])

    questions = load_questions()

    # Initialize session state for selected question ID
    if 'selected_question_id' not in st.session_state:
        st.session_state.selected_question_id = questions[0]['id'] if questions else None

    # Sidebar options
    st.sidebar.header("Settings")

    # Select a programming language
    language = st.sidebar.selectbox("Select Language", options.ace_languages)

    # Select an Ace Editor theme
    theme = st.sidebar.selectbox("Select Theme", options.ace_themes, index=options.ace_themes.index('dracula'))

    # Select an Ace Editor keybinding
    keybinding = st.sidebar.selectbox("Select Keybinding", options.ace_keybindings, index=options.ace_keybindings.index('ace'))

    # Font size selection
    st.sidebar.subheader("Font Size")
    font_size_col1, font_size_col2 = st.sidebar.columns([3, 1])
    with font_size_col1:
        st.sidebar.slider(
            "Font Size",
            min_value=10,
            max_value=24,
            key='font_size_slider',
            on_change=font_size_slider_changed,
        )
    with font_size_col2:
        st.sidebar.number_input(
            label="",
            min_value=10,
            max_value=24,
            key='font_size_input',
            label_visibility="collapsed",
            step=1,
            on_change=font_size_input_changed,
        )

    # Editor height selection
    st.sidebar.subheader("Editor Height")
    editor_height_col1, editor_height_col2 = st.sidebar.columns([3, 1])
    with editor_height_col1:
        st.sidebar.slider(
            "Editor Height",
            min_value=200,
            max_value=1000,
            key='editor_height_slider',
            on_change=editor_height_slider_changed,
        )
    with editor_height_col2:
        st.sidebar.number_input(
            label="",
            min_value=200,
            max_value=1000,
            key='editor_height_input',
            label_visibility="collapsed",
            step=50,
            on_change=editor_height_input_changed,
        )

    # Get the values for the editor settings
    font_size = st.session_state.font_size_slider
    editor_height = st.session_state.editor_height_slider

    # Sidebar options for questions
    st.sidebar.header("Questions")

    # Toggle to show/hide the question overlay
    show_question = st.sidebar.checkbox("Show Question", value=False)

    # Select a question
    if questions:
        # Map titles to question IDs
        title_to_id = {f"{q['id']}. {q['title']} ({q['difficulty']})": q['id'] for q in questions}
        question_titles = list(title_to_id.keys())
        selected_index = next((i for i, q in enumerate(questions) if q['id'] == st.session_state.selected_question_id), 0)
        selected_question_title = st.sidebar.selectbox("Select Question", question_titles, index=selected_index)
        st.session_state.selected_question_id = title_to_id[selected_question_title]
    else:
        st.sidebar.write("No questions available.")

    # Function to get the selected question
    def get_selected_question():
        for q in questions:
            if q['id'] == st.session_state.selected_question_id:
                return q
        return None

    # Initialize session state for code and output
    if 'code' not in st.session_state or st.session_state.language != language:
        # If there's starter code from the question, use it
        selected_question = get_selected_question()
        if selected_question and 'starter_code' in selected_question:
            st.session_state.code = selected_question['starter_code'].get(language, options.default_code_snippets.get(language, ''))
        else:
            st.session_state.code = options.default_code_snippets.get(language, '')
        st.session_state.language = language  # Store current language in session state

    if 'output' not in st.session_state:
        st.session_state.output = ''

    # Use st.columns to create a layout
    if show_question:
        col1, col2 = st.columns([3, 2])

        # Code editor and run button in the first column
        with col1:
            code = st_ace(
                value=st.session_state.code,
                language=language,
                theme=theme,
                keybinding=keybinding,
                key='ace-editor',
                auto_update=True,
                height=int(editor_height),
                font_size=int(font_size),
                wrap=True,
                show_gutter=True,
                show_print_margin=False,
            )

            # Update session_state.code if code is not None
            if code is not None:
                st.session_state.code = code

            # Button to run the code
            if st.button('Run'):
                # Map Ace Editor language to execution language
                exec_language = options.execution_languages.get(language, None)
                if exec_language:
                    st.session_state.output = execute_code(st.session_state.code, exec_language)
                else:
                    st.session_state.output = f"Execution for {language} is not supported yet."

            # Display the output in a terminal-like box
            st.subheader("Output")
            escaped_output = html.escape(st.session_state.output)  # Escape HTML special characters
            st.markdown(f"<div class='terminal'>{escaped_output}</div>", unsafe_allow_html=True)

        # Display the question in the second column
        with col2:
            selected_question = get_selected_question()
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
    else:
        # Full-width code editor when the question is not displayed
        code = st_ace(
            value=st.session_state.code,
            language=language,
            theme=theme,
            keybinding=keybinding,
            key='ace-editor',
            auto_update=True,
            height=int(editor_height),
            font_size=int(font_size),
            wrap=True,
            show_gutter=True,
            show_print_margin=False,
        )

        # Update session_state.code if code is not None
        if code is not None:
            st.session_state.code = code

        # Button to run the code
        if st.button('Run'):
            # Map Ace Editor language to execution language
            exec_language = options.execution_languages.get(language, None)
            if exec_language:
                st.session_state.output = execute_code(st.session_state.code, exec_language)
            else:
                st.session_state.output = f"Execution for {language} is not supported yet."

        # Display the output in a terminal-like box
        st.subheader("Output")
        escaped_output = html.escape(st.session_state.output)  # Escape HTML special characters
        st.markdown(f"<div class='terminal'>{escaped_output}</div>", unsafe_allow_html=True)

    # Add custom CSS to style the terminal-like output
    st.markdown(
        """
        <style>
        /* Style for the terminal-like output */
        .terminal {
            background-color: #1e1e1e;
            color: #d4d4d4;
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
            white-space: pre-wrap;
            overflow: auto;
            height: 300px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()