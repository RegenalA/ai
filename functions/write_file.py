import os
from google.genai import types
def write_file(working_directory, file_path, content):
    try:
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_file = os.path.commonpath([abs_path, target_file]) == abs_path
        if valid_target_file is False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file) is True:
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        par_dir = os.path.dirname(target_file)
        os.makedirs(par_dir, exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path","content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file whose contents should be written or overwritten, relative to the working directory"),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Contents that should be written"
            ),
        },
    ),
)
     
