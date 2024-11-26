from .execute_python_code import execute_python_code, run_test_cases
from .execute_cpp_code import execute_cpp_code

# def execute_code(code, language):
#     """
#     Executes the provided code based on the specified language.
#     """
#     if language == "python":
#         result = execute_python_code(code)
#         return result
#     elif language == "c_cpp":
#         result = execute_cpp_code(code)
#         return result
#     else:
#         return f"Execution for {language} is not supported yet."

def execute_code(code, language, test_cases=None):
    """
    Executes the provided code based on the specified language.
    If test_cases is provided, it runs the code against them.
    """
    if language == "python":
        if test_cases:
            results = run_test_cases(code, test_cases)
            return results
        else:
            result = execute_python_code(code)
            return result
    elif language == "c_cpp":
        # Similar implementation for C++
        pass  # Placeholder
    else:
        return f"Execution for {language} is not supported yet."
