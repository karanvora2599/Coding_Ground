# executor/execute_python_code.py

import io
import contextlib
import sys
import threading
import ast

# Check if the 'resource' module is available
try:
    import resource

    def limit_resources():
        # Limit CPU time (in seconds)
        resource.setrlimit(resource.RLIMIT_CPU, (2, 2))
        # Limit memory usage (in bytes)
        resource.setrlimit(resource.RLIMIT_AS, (50 * 1024 * 1024, 50 * 1024 * 1024))  # 50MB
except ImportError:
    # Define a fallback for Windows or other systems where `resource` is unavailable
    def limit_resources():
        # No-op function: limits are not applied on Windows
        pass

def is_safe_code(code):
    forbidden_keywords = [
        'import os', 'import sys', 'open', 'exec', 'eval', 'subprocess', 
        'compile', '__import__', 'globals', 'locals', 'exit', 'quit', 
        'getattr', 'setattr', 'delattr', 'input'
    ]
    return not any(keyword in code for keyword in forbidden_keywords)

def is_safe_ast(code):
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Lambda)):
                return False
        return True
    except SyntaxError:
        return False

def execute_with_timeout(code, globals, timeout=2):
    f = io.StringIO()
    def target():
        try:
            with contextlib.redirect_stdout(f):
                exec(code, globals)
        except Exception as e:
            f.write(f"Error: {e}")

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout=timeout)
    if thread.is_alive():
        return "Error: Execution timed out."
    return f.getvalue()

def execute_python_code(code):
    if not is_safe_code(code) or not is_safe_ast(code):
        return "Error: Unsafe code detected or function/class/lambda definitions are not allowed."

    try:
        allowed_modules = {
            'numpy': __import__('numpy'),
            'pandas': __import__('pandas'),
            'math': __import__('math'),
            'random': __import__('random'),
        }

        def restricted_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name in allowed_modules:
                return allowed_modules[name]
            else:
                raise ImportError(f"Importing module '{name}' is not allowed.")

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
            '__import__': restricted_import,
        }

        restricted_globals = {
            '__builtins__': safe_builtins,
        }

        restricted_globals.update(allowed_modules)

        sys.setrecursionlimit(50)  # Set recursion limit
        limit_resources()  # Apply resource limits if available

        # Execute the code with timeout and capture the result
        result = execute_with_timeout(code, restricted_globals)
        return result
    except Exception as e:
        return f"Error: {e}"
