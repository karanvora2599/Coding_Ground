import subprocess
import tempfile
import os

def execute_cpp_code(code):
    try:
        with tempfile.TemporaryDirectory() as tmpdirname:
            source_file = os.path.join(tmpdirname, 'temp.cpp')
            executable = os.path.join(tmpdirname, 'temp')

            with open(source_file, 'w') as f:
                f.write(code)

            compile_process = subprocess.run(
                ['g++', source_file, '-o', executable],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10
            )

            if compile_process.returncode != 0:
                return f"Compilation Error:\n{compile_process.stderr}"

            run_process = subprocess.run(
                [executable],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )

            if run_process.returncode != 0:
                return f"Runtime Error:\n{run_process.stderr}"

            return run_process.stdout

    except subprocess.TimeoutExpired:
        return "Error: Execution timed out."
    except Exception as e:
        return f"Error: {e}"