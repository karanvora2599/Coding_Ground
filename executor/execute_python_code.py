# import io
# import contextlib
# import sys
# import threading
# import ast
# import json

# # Check if the 'resource' module is available
# try:
#     import resource

#     def limit_resources():
#         # Limit CPU time (in seconds)
#         resource.setrlimit(resource.RLIMIT_CPU, (2, 2))
#         # Limit memory usage (in bytes)
#         resource.setrlimit(resource.RLIMIT_AS, (50 * 1024 * 1024, 50 * 1024 * 1024))  # 50MB
# except ImportError:
#     # Define a fallback for Windows or other systems where `resource` is unavailable
#     def limit_resources():
#         # No-op function: limits are not applied on Windows
#         pass

# def is_safe_code(code):
#     forbidden_keywords = [
#         'import os', 'import sys', 'open', 'exec', 'eval', 'subprocess', 
#         'compile', '__import__', 'globals', 'locals', 'exit', 'quit', 
#         'getattr', 'setattr', 'delattr', 'input'
#     ]
#     return not any(keyword in code for keyword in forbidden_keywords)

# def is_safe_ast(code):
#     try:
#         tree = ast.parse(code)
#         for node in ast.walk(tree):
#             if isinstance(node, (ast.ClassDef, ast.Lambda)):
#                 return False
#         return True
#     except SyntaxError:
#         return False

# def execute_with_timeout(code, globals, timeout=2):
#     f = io.StringIO()
#     def target():
#         try:
#             with contextlib.redirect_stdout(f):
#                 exec(code, globals)
#         except Exception as e:
#             f.write(f"Error: {e}")
#     thread = threading.Thread(target=target)
#     thread.start()
#     thread.join(timeout=timeout)
#     if thread.is_alive():
#         return "Error: Execution timed out."
#     return f.getvalue()

# def execute_python_code(code, func_name=None, func_args=None):
#     if not is_safe_code(code) or not is_safe_ast(code):
#         return "Error: Unsafe code detected or class/lambda definitions are not allowed."
#     try:
#         allowed_modules = {
#             'json': __import__('json'),
#             'math': __import__('math'),
#             'random': __import__('random'),
#         }
#         def restricted_import(name, globals=None, locals=None, fromlist=(), level=0):
#             if name in allowed_modules:
#                 return allowed_modules[name]
#             else:
#                 raise ImportError(f"Importing module '{name}' is not allowed.")
#         safe_builtins = {
#             'print': print,
#             'len': len,
#             'range': range,
#             'str': str,
#             'int': int,
#             'float': float,
#             'bool': bool,
#             'list': list,
#             'dict': dict,
#             'set': set,
#             'tuple': tuple,
#             'enumerate': enumerate,
#             'zip': zip,
#             'abs': abs,
#             'min': min,
#             'max': max,
#             'sum': sum,
#             'sorted': sorted,
#             '__import__': restricted_import,
#             'json': allowed_modules['json'],
#         }
#         restricted_globals = {
#             '__builtins__': safe_builtins,
#         }
#         restricted_globals.update(allowed_modules)
#         sys.setrecursionlimit(50)  # Set recursion limit
#         limit_resources()  # Apply resource limits if available
#         if func_name and func_args is not None:
#             # Execute the user's code to define the function
#             exec(code, restricted_globals)
#             # Now, call the function with the provided arguments
#             f = io.StringIO()
#             with contextlib.redirect_stdout(f):
#                 result = restricted_globals[func_name](*func_args)
#                 print(json.dumps(result))
#             return f.getvalue()
#         else:
#             # Execute the code with timeout and capture the result
#             result = execute_with_timeout(code, restricted_globals)
#             return result
#     except Exception as e:
#         return f"Error: {e}"

# def run_test_cases(code, test_cases):
#     import json
#     results = []
#     for idx, test_case in enumerate(test_cases):
#         input_data = test_case['input']
#         expected_output = test_case['expected_output']
#         # Prepare function arguments as a list
#         func_args = []
#         for arg in test_case['input'].values():
#             func_args.append(arg)
#         # Execute the code and get the output
#         output = execute_python_code(code, func_name='two_sum', func_args=func_args)
#         # Parse the output
#         try:
#             actual_output = json.loads(output.strip())
#             # Compare actual output with expected output
#             if actual_output == expected_output:
#                 results.append({'test_case': idx + 1, 'status': 'Passed'})
#             else:
#                 results.append({'test_case': idx + 1, 'status': 'Failed', 'expected': expected_output, 'actual': actual_output})
#         except json.JSONDecodeError:
#             # If output is not valid JSON, consider it as failed
#             results.append({'test_case': idx + 1, 'status': 'Error', 'message': output.strip()})
#     return results

# execute_python_code.py

import io
import contextlib
import sys
import multiprocessing
import ast
import json
import traceback

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
        'getattr', 'setattr', 'delattr', 'input', 'threading', 'multiprocessing'
    ]
    return not any(keyword in code for keyword in forbidden_keywords)

def is_safe_ast(code):
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.Lambda)):
                return False
        return True
    except SyntaxError:
        return False

# Move 'run_user_code' to the top level
def run_user_code(code, func_name, func_args, return_dict):
    try:
        limit_resources()  # Apply resource limits if available

        allowed_modules = {
            'json': __import__('json'),
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
            'json': allowed_modules['json'],
        }

        restricted_globals = {
            '__builtins__': safe_builtins,
        }
        restricted_globals.update(allowed_modules)
        sys.setrecursionlimit(50)  # Set recursion limit

        if func_name and func_args is not None:
            # Execute the user's code to define the function
            exec(code, restricted_globals)
            # Now, call the function with the provided arguments
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                result = restricted_globals[func_name](*func_args)
                print(json.dumps(result))
            return_dict['output'] = f.getvalue()
        else:
            # Execute the code and capture the result
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                exec(code, restricted_globals)
            return_dict['output'] = f.getvalue()
    except Exception as e:
        return_dict['output'] = f"Error: {e}"

def execute_python_code(code, func_name=None, func_args=None):
    if not is_safe_code(code) or not is_safe_ast(code):
        return "Error: Unsafe code detected or class/lambda definitions are not allowed."

    # Use multiprocessing to run the code in a separate process
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    # Create the process with the top-level 'run_user_code' function
    p = multiprocessing.Process(target=run_user_code, args=(code, func_name, func_args, return_dict))
    p.start()
    p.join(timeout=5)  # Limit total execution time to 5 seconds

    if p.is_alive():
        p.terminate()
        return "Error: Execution timed out."
    else:
        return return_dict.get('output', 'Error: No output returned.')

def run_test_cases(code, test_cases):
    results = []
    for idx, test_case in enumerate(test_cases):
        input_data = test_case['input']
        expected_output = test_case['expected_output']
        # Prepare function arguments as a list
        func_args = []
        for arg in test_case['input'].values():
            func_args.append(arg)
        # Execute the code and get the output
        output = execute_python_code(code, func_name='two_sum', func_args=func_args)
        # Parse the output
        try:
            actual_output = json.loads(output.strip())
            # Compare actual output with expected output
            if actual_output == expected_output:
                results.append({'test_case': idx + 1, 'status': 'Passed'})
            else:
                results.append({'test_case': idx + 1, 'status': 'Failed', 'expected': expected_output, 'actual': actual_output})
        except json.JSONDecodeError:
            # If output is not valid JSON, consider it as failed
            results.append({'test_case': idx + 1, 'status': 'Error', 'message': output.strip()})
    return results