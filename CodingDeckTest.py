import streamlit as st
import streamlit.components.v1 as components

# Function to load the Ace Editor
def ace_editor(default_code="print('Hello, Streamlit!')"):
    # A placeholder to store the editor content
    editor_content = st.empty()
    # HTML and JavaScript for Ace Editor
    html_code = f"""
    <div id="editor" style="height: 300px; width: 100%;">{default_code}</div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ace.js"></script>
    <script>
        const editor = ace.edit("editor");
        editor.setTheme("ace/theme/dracula");
        editor.session.setMode("ace/mode/python");
        editor.setOptions({{
            fontSize: "14px",
            enableBasicAutocompletion: true,
            enableLiveAutocompletion: true,
        }});

        // Periodically send the editor content to Streamlit
        function sendEditorContent() {{
            const editorContent = editor.getValue();
            const streamlitMessage = {{
                isStreamlitMessage: true,
                type: "streamlit:setComponentValue",
                value: editorContent
            }};
            window.parent.postMessage(streamlitMessage, "*");
        }}

        setInterval(sendEditorContent, 500);
    </script>
    """

    # Render the HTML in Streamlit
    components.html(html_code, height=300)

# Main Streamlit application
st.title("Streamlit with Ace Editor (Python)")

# Show Ace Editor and capture code
ace_editor()

# Retrieve editor content using a Streamlit state variable
if 'editor_content' not in st.session_state:
    st.session_state.editor_content = ""

code = st.session_state.editor_content

# Button to run the code
if st.button('Run'):
    st.subheader("Editor Content")
    st.code(code, language='python')

    st.subheader("Output")
    try:
        # Redirect stdout to capture print statements
        import io
        import contextlib
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            exec(code, {})
        output = f.getvalue()
        st.text(output)
    except Exception as e:
        st.error(f"Error: {e}")