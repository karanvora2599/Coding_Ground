from executor.execute_python_code import execute_python_code
from executor.execute_cpp_code import execute_cpp_code

def execute_code(code, language):
    if language == "python":
        return execute_python_code(code)
    elif language == "c_cpp":
        return execute_cpp_code(code)
    else:
        return f"Execution for {language} is not supported yet."