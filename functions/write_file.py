import os

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
        return f"Error: Unable to access directory {file_path}"
    except FileNotFoundError:
        return f"Error: Unable to write contents as {file_path} does not exist"
    except Exception:
        return f"Error: Unable to access {file_path}"
