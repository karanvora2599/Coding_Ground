# main_app.py

import streamlit as st
from streamlit_ace import st_ace
from executor import execute_code

# Main Streamlit application
def main():
    st.title("Streamlit with Ace Editor")

    # Select a programming language
    language = st.selectbox("Select Language", ["python", "c_cpp"])

    # Initialize session state for code and output
    if 'code' not in st.session_state:
        if language == "python":
            st.session_state.code = "print('Hello, Streamlit!')"
        elif language == "c_cpp":
            st.session_state.code = """#include <iostream>

int main() {
    std::cout << "Hello, C++!" << std::endl;
    return 0;
}
"""
        else:
            st.session_state.code = ""

    if 'output' not in st.session_state:
        st.session_state.output = ''

    # Show Ace Editor and capture code
    code = st_ace(
        value=st.session_state.code,
        language=language,
        theme='dracula',
        key=f'ace-editor-{language}',
        auto_update=True,
        height=300,
    )

    # Update session_state.code if code is not None
    if code is not None:
        st.session_state.code = code

    # Button to run the code
    if st.button('Run'):
        st.session_state.output = execute_code(st.session_state.code, language)

    # Display the output
    st.subheader("Output")
    st.text(st.session_state.output)

if __name__ == "__main__":
    main()