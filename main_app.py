import streamlit as st
from streamlit_ace import st_ace
from executor import execute_code
import html

# Set the page configuration to wide layout
st.set_page_config(layout="wide")

# List of available themes for Ace Editor
ace_themes = [
    'chrome', 'clouds', 'crimson_editor', 'dawn', 'dreamweaver',
    'eclipse', 'github', 'iplastic', 'solarized_light', 'textmate',
    'tomorrow', 'xcode', 'kuroir', 'katzenmilch', 'sqlserver',
    'ambiance', 'chaos', 'clouds_midnight', 'cobalt', 'gruvbox',
    'idle_fingers', 'kr_theme', 'merbivore', 'merbivore_soft',
    'mono_industrial', 'monokai', 'pastel_on_dark', 'solarized_dark',
    'terminal', 'tomorrow_night', 'tomorrow_night_blue',
    'tomorrow_night_bright', 'tomorrow_night_eighties', 'twilight',
    'dracula', 'gob', 'vibrant_ink'
]

# List of programming languages supported by Ace Editor
ace_languages = [
    'python', 'c_cpp', 'java', 'javascript', 'ruby', 'rust', 'go',
    'csharp', 'kotlin', 'swift', 'php', 'perl', 'r', 'typescript',
    'sql', 'html', 'css', 'markdown', 'json', 'xml', 'yaml', 'sh'
]

# Mapping from Ace Editor language names to execution function languages
execution_languages = {
    'python': 'python',
    'c_cpp': 'c_cpp',
    'java': 'java',
    'javascript': 'javascript',
    # Add other mappings as needed
}

# Default code snippets for each language
default_code_snippets = {
    'python': "print('Hello, Streamlit!')",
    'c_cpp': """#include <iostream>

int main() {
    std::cout << "Hello, C++!" << std::endl;
    return 0;
}
""",
    'java': """public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, Java!");
    }
}
""",
    'javascript': "console.log('Hello, JavaScript!');",
    'ruby': "puts 'Hello, Ruby!'",
    'go': """package main

import "fmt"

func main() {
    fmt.Println("Hello, Go!")
}
""",
    # Add default code for other languages as needed
}

# List of available keybindings for Ace Editor
ace_keybindings = ['vscode', 'ace', 'vim', 'emacs', 'sublime']

def main():
    st.title("Coding Grounds")

    # Sidebar options
    st.sidebar.header("Settings")

    # Select a programming language
    language = st.sidebar.selectbox("Select Language", ace_languages)

    # Select an Ace Editor theme
    theme = st.sidebar.selectbox("Select Theme", ace_themes, index=ace_themes.index('dracula'))

    # Select an Ace Editor keybinding
    keybinding = st.sidebar.selectbox("Select Keybinding", ace_keybindings)

    # Font size selection
    st.sidebar.subheader("Font Size")
    font_size_col1, font_size_col2 = st.sidebar.columns([3, 1])
    with font_size_col1:
        font_size = st.slider("Font Size", min_value=10, max_value=24, value=14, key='font_size_slider')
    with font_size_col2:
        font_size_input = st.number_input(
            label=" ",
            min_value=10,
            max_value=24,
            value=font_size,
            key='font_size_input',
            label_visibility="collapsed",
            step=1
        )
    # Synchronize slider and input
    if font_size != font_size_input:
        font_size = font_size_input

    # Editor height selection
    st.sidebar.subheader("Editor Height")
    editor_height_col1, editor_height_col2 = st.sidebar.columns([3, 1])
    with editor_height_col1:
        editor_height = st.slider("Editor Height", min_value=200, max_value=1000, value=600, key='editor_height_slider')
    with editor_height_col2:
        editor_height_input = st.number_input(
            label=" ",
            min_value=200,
            max_value=1000,
            value=editor_height,
            key='editor_height_input',
            label_visibility="collapsed",
            step=50
        )
    # Synchronize slider and input
    if editor_height != editor_height_input:
        editor_height = editor_height_input

    # Initialize session state for code and output
    if 'code' not in st.session_state or st.session_state.language != language:
        st.session_state.code = default_code_snippets.get(language, '')
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
            key='ace-editor',  # Simplified key to prevent unnecessary re-initialization
            auto_update=True,
            height=int(editor_height),
            font_size=int(font_size),
            wrap=True,  # Enable code wrapping
            show_gutter=True,
            show_print_margin=False,
        )

    # Update session_state.code if code is not None
    if code is not None:
        st.session_state.code = code

    # Button to run the code
    if st.button('Run'):
        # Map Ace Editor language to execution language
        exec_language = execution_languages.get(language)
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