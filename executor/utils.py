import ast

def is_safe_code(code):
    forbidden_keywords = ['import os', 'open', 'exec', 'eval', 'subprocess']
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