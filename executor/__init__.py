# executor/__init__.py

from .execute_python_code import execute_python_code
from .execute_cpp_code import execute_cpp_code

def execute_code(code, language):
    """
    Executes the provided code based on the specified language.
    """
    # print("execute_code called with language:", language)  # Debug print
    if language == "python":
        result = execute_python_code(code)
        return result
    elif language == "c_cpp":
        result = execute_cpp_code(code)
        return result
    else:
        return f"Execution for {language} is not supported yet."