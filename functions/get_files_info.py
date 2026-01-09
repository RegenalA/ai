import os
from google.genai import types
def get_files_info(working_directory, directory="."):
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, directory))
        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path
        if valid_target_dir is False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir) is False:
            return f'Error: "{directory}" is not a directory'
        file_info_list = []
        for filename in os.listdir(target_dir):
            file_info = f'- {filename}: file_size={os.path.getsize(os.path.join(target_dir, filename))}, is_dir={os.path.isdir(os.path.join(target_dir, filename))}'
            file_info_list.append(file_info)
        return "\n".join(file_info_list)
    except Exception as e:
        return f"Error: {e}"
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

