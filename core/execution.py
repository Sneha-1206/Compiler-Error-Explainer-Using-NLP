import subprocess
import tempfile
import os

def run_python_code(code):
    try:
        exec(code)
        return None
    except Exception as e:
        return str(e)

def run_cpp_code(code):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp") as f:
            f.write(code.encode())
            filename = f.name

        exe_file = filename + ".out"

        compile_proc = subprocess.run(
            ["g++", filename, "-o", exe_file],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

        if compile_proc.returncode != 0:
            os.remove(filename)
            return compile_proc.stderr.decode()

        run_proc = subprocess.run(
            [exe_file],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            timeout=5
        )

        os.remove(filename)
        os.remove(exe_file)

        return None

    except Exception as e:
        return str(e)