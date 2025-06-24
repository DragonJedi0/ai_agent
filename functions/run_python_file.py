import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)

    if not file_path or file_path == ".":
        file_path = working_directory
    
    file = file_path
    
    if file_path and not file_path.startswith("/"):
        file_path = working_directory + "/" + file_path

    file_path = os.path.abspath(file_path)

    if not file_path.startswith(working_directory):
        return f'Error: Cannot execute "{file}" as it is outside the permitted working directory'

    if not os.path.exists(file_path):
        return f'Error: File "{file}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file}" is not a Python file.'

    try:
        output = subprocess.run(["python3", f"{file_path}"], cwd=working_directory, capture_output=True, timeout=30)
        if not output.stdout and not output.stderr:
            return "No output produced"

        msg = f"Ran {file_path}\nSTDOUT: {output.stdout}\nSTDERR: {output.stderr}"
        if not output.returncode == 0:
            msg += f"\nProcess exited with code {output.returncode}"

        return msg

    except PermissionError:
        return f"Error: Unable to access {file_path}"
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to locate and execute the file from, relative to the working directory. If not provided, assume file is in the working directory itself.",
            ),
        },
    ),
)
