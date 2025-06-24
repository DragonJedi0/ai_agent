import os
from google.genai import types

def write_file(working_directory, file_path, content):
    working_directory = os.path.abspath(working_directory)

    if not file_path or file_path == ".":
        file_path = working_directory
    
    if file_path and not file_path.startswith("/"):
        file_path = working_directory + "/" + file_path

    file_path = os.path.abspath(file_path)

    if not file_path.startswith(working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except PermissionError:
        return f"Error: Unable to access {file_path}"
    except FileNotFoundError:
        return f"Error: Unable to write contents to {file_path} because path does not exist"
    except Exception:
        return f"Error: Unable to access {file_path}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write contents to a file in the requested file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to where the file will be saved, relative to the working directory. If not provided, save the file in the working directory itself.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents of the file provided by the user.",
            ),
        },
    ),
)
