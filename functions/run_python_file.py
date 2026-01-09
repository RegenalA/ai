import os
import subprocess
from google.genai import types
def run_python_file(working_directory, file_path, args=None):
    try:
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_file = os.path.commonpath([abs_path, target_file]) == abs_path
        if valid_target_file is False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_file) is False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if target_file.endswith(".py") is False:
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file]
        if args is not None:
            command.extend(args)
        result = subprocess.run(
            command,
            cwd=abs_path,
            capture_output=True,
            text=True,
            timeout=30,
)
        output = ""

        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"

        if not result.stdout and not result.stderr:
            output += "No output produced"
        else:
            if result.stdout:
                output += f"STDOUT:{result.stdout}"
            if result.stderr:
                output += f"STDERR:{result.stderr}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"  
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file whose contents should be executed, relative to the working directory"),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional arguments"
            ),
        },
    ),
)

