# main_app.py

import streamlit as st
from streamlit_ace import st_ace
from executor import execute_code

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

def main():
    st.title("Streamlit with Ace Editor")

    # Sidebar options
    st.sidebar.header("Settings")

    # Select a programming language
    language = st.sidebar.selectbox("Select Language", ace_languages)

    # Select an Ace Editor theme
    theme = st.sidebar.selectbox("Select Theme", ace_themes, index=ace_themes.index('dracula'))

    # Initialize session state for code and output
    if 'code' not in st.session_state or st.session_state.language != language:
        st.session_state.code = default_code_snippets.get(language, '')
        st.session_state.language = language  # Store current language in session state

    if 'output' not in st.session_state:
        st.session_state.output = ''

    # Show Ace Editor and capture code
    code = st_ace(
        value=st.session_state.code,
        language=language,
        theme=theme,
        key=f'ace-editor-{language}-{theme}',
        auto_update=True,
        height=400,
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

    # Display the output
    st.subheader("Output")
    st.text(st.session_state.output)

if __name__ == "__main__":
    main()