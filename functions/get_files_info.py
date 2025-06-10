import os

def get_files_info(working_directory, directory=None):
    working_directory = os.path.abspath(working_directory)

    if not directory or directory == ".":
        directory = working_directory
    
    if directory and not directory.startswith("/"):
        directory = working_directory + "/" + directory

    directory = os.path.abspath(directory)

    if not directory.startswith(working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'

    try:
        # Get a list of items in the source directory
        contents = os.listdir(directory)
        output = ""
        for object in contents:
            # Build the full source path for the item
            current_path = os.path.join(directory, object)
            try:
                output += f"- {object}: file_size={os.path.getsize(current_path)} bytes, is_dir={os.path.isdir(current_path)}\n"
            except:
                continue

        return output

    except PermissionError:
        return f"Error: Unable to access directory {directory}"
    except Exception:
        return f"Error: Unable to read contents of {directory}"
