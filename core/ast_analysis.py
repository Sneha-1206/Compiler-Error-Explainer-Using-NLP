import ast
import subprocess

def extract_python_context(code):
    try:
        ast.parse(code)
        return "Code is syntactically valid"
    except SyntaxError as e:
        return f"Syntax Error at line {e.lineno}: {e.msg}"

def analyze_code(code):
    errors = []

    try:
        ast.parse(code)
    except SyntaxError as e:
        errors.append(f"Syntax Error (Line {e.lineno}): {e.msg}")
        return errors

    for i, line in enumerate(code.split("\n"), 1):
        try:
            subprocess.run(["python3", line], timeout=5)
        except Exception as e:
            errors.append(f"Runtime Error (Line {i}): {str(e)}")

    return errors