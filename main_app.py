import streamlit as st
from streamlit_ace import st_ace
from executor import execute_code
import html
import options

# Set the page configuration to wide layout
st.set_page_config(layout="wide")

def main():
    st.title("Coding Grounds")

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
    font_size = st.sidebar.slider("Font Size", min_value=10, max_value=24, value=14, key='font_size_slider')

    # Editor height selection
    st.sidebar.subheader("Editor Height")
    editor_height = st.sidebar.slider("Editor Height", min_value=200, max_value=1000, value=600, key='editor_height_slider')

    # Initialize session state for code and output
    if 'code' not in st.session_state or st.session_state.language != language:
        st.session_state.code = options.default_code_snippets.get(language, '')
        st.session_state.language = language  # Store current language in session state

    if 'output' not in st.session_state:
        st.session_state.output = ''

    # Add custom CSS to adjust the width of the Ace Editor and style the output terminal
    st.markdown(
        """
        <style>
        /* Adjust the width of the Ace Editor container */
        .ace_editor {
            width: 100% !important;
        }
        /* Remove padding/margin from the code editor */
        .st-ace {
            padding: 0;
        }
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

    # Use st.container to contain the editor
    with st.container():
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

if __name__ == "__main__":
    main()