import streamlit as st
import streamlit.components.v1 as components

# Define the custom component function
def st_ace_editor(content="", language="python", theme="dracula", key=None):
    # Use declare_component to create a bidirectional component
    component_value = components.declare_component(
        "ace_editor",
        path="./components/ace_editor",
    )(
        content=content,
        language=language,
        theme=theme,
        key=key,
        default=content,
    )
    return component_value