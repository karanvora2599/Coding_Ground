# javascript/features.py

import streamlit as st
from . import options

def inject_javascript():
    js_code = ""

    # Feature: Disable copy-paste in the code editor
    if options.DISABLE_COPY_PASTE:
        js_code += """
        <script>
        // Function to disable copy, cut, and paste in the Ace Editor
        function disableCopyPaste() {
            // Wait until the Ace Editor is available
            const checkEditor = setInterval(function() {
                const editorElement = document.querySelector('.ace_editor');
                if (editorElement && window.ace) {
                    clearInterval(checkEditor);
                    const editor = ace.edit(editorElement);

                    // Disable keyboard shortcuts
                    editor.commands.bindKey("Ctrl-C", null);
                    editor.commands.bindKey("Command-C", null);
                    editor.commands.bindKey("Ctrl-X", null);
                    editor.commands.bindKey("Command-X", null);
                    editor.commands.bindKey("Ctrl-V", null);
                    editor.commands.bindKey("Command-V", null);

                    // Disable context menu
                    editor.container.addEventListener('contextmenu', function(e) {
                        e.preventDefault();
                    });

                    // Disable drag and drop
                    editor.container.addEventListener('dragover', function(e) {
                        e.preventDefault();
                    });
                    editor.container.addEventListener('drop', function(e) {
                        e.preventDefault();
                    });

                    // Disable paste via mouse
                    editor.on('paste', function(e) {
                        e.text = '';
                        e.cancel();
                        return false;
                    });
                }
            }, 100);
        }

        document.addEventListener('DOMContentLoaded', function() {
            disableCopyPaste();
        });
        </script>
        """

    # Feature: Show a warning when the user switches tabs
    if options.SHOW_TAB_SWITCH_WARNING:
        js_code += """
        <script>
        // Function to show the tab switch warning popup
        function showTabSwitchWarning() {
            // Create the popup element
            var popup = document.createElement('div');
            popup.id = 'tab-switch-warning';
            popup.style.position = 'fixed';
            popup.style.top = '50%';
            popup.style.left = '50%';
            popup.style.transform = 'translate(-50%, -50%)';
            popup.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
            popup.style.color = 'white';
            popup.style.padding = '20px';
            popup.style.borderRadius = '10px';
            popup.style.zIndex = '1000';
            popup.style.textAlign = 'center';
            popup.style.fontSize = '20px';
            popup.innerHTML = 'You have switched tabs! Please stay focused.';

            // Append the popup to the body
            document.body.appendChild(popup);

            // Remove the popup after 10 seconds
            setTimeout(function() {
                if (popup.parentNode) {
                    popup.parentNode.removeChild(popup);
                }
            }, 10000); // 10000 milliseconds = 10 seconds
        }

        document.addEventListener('visibilitychange', function() {
            if (document.hidden) {
                // User has switched tabs
                showTabSwitchWarning();
            }
        });
        </script>
        """
    
    # Inject the JavaScript code into the Streamlit app
    if js_code:
        st.markdown(js_code, unsafe_allow_html=True)