# executor.py

import subprocess
import io
import contextlib
import sys
import tempfile
import os

def execute_code(code, language):
    if language == "python":
        return execute_python_code(code)
    elif language == "c_cpp":
        return execute_cpp_code(code)
    else:
        return f"Execution for {language} is not supported yet."

def execute_python_code(code):
    """
    Executes Python code in a restricted environment, allowing imports of specific modules.
    """
    f = io.StringIO()
    try:
        # Allowed modules
        allowed_modules = {
            'numpy': __import__('numpy'),
            'pandas': __import__('pandas'),
            'math': __import__('math'),
            'random': __import__('random'),
        }

        # Create a custom __import__ function
        def restricted_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name in allowed_modules:
                return allowed_modules[name]
            elif name in safe_builtins:
                # Allow importing built-in modules like 'math' if needed
                return __import__(name)
            else:
                raise ImportError(f"Importing module '{name}' is not allowed.")

        # Define a whitelist of safe built-in functions
        safe_builtins = {
            'print': print,
            'len': len,
            'range': range,
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'list': list,
            'dict': dict,
            'set': set,
            'tuple': tuple,
            'enumerate': enumerate,
            'zip': zip,
            'abs': abs,
            'min': min,
            'max': max,
            'sum': sum,
            'sorted': sorted,
            # '__import__' will be added after defining restricted_import
        }

        # Assign the restricted_import function to '__import__' in safe_builtins
        safe_builtins['__import__'] = restricted_import

        # Create a restricted execution environment
        restricted_globals = {
            '__builtins__': safe_builtins,
        }

        # Add allowed modules to the restricted globals
        restricted_globals.update(allowed_modules)

        # Execute the code with restricted globals
        with contextlib.redirect_stdout(f):
            exec(code, restricted_globals, {})
        output = f.getvalue()
        return output
    except Exception as e:
        return f"Error: {e}"

def execute_cpp_code(code):
    """
    Executes C++ code by compiling and running it.
    """
    try:
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as tmpdirname:
            source_file = os.path.join(tmpdirname, 'temp.cpp')
            executable = os.path.join(tmpdirname, 'temp')

            # Write the code to a file
            with open(source_file, 'w') as f:
                f.write(code)

            # Compile the code
            compile_process = subprocess.run(
                ['g++', source_file, '-o', executable],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10  # Compilation timeout
            )

            if compile_process.returncode != 0:
                return f"Compilation Error:\n{compile_process.stderr}"

            # Run the executable
            run_process = subprocess.run(
                [executable],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5  # Execution timeout
            )

            if run_process.returncode != 0:
                return f"Runtime Error:\n{run_process.stderr}"

            return run_process.stdout

    except subprocess.TimeoutExpired:
        return "Error: Execution timed out."
    except Exception as e:
        return f"Error: {e}"