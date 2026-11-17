import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file within the working directory and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python script",
                },
            },
            "required": ["file_path"],
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
    if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file.'
    if not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    command = ["python", target_file]
    if args:
        command.extend(args)
    try:
        output_string = f'"{file_path}" was executed with success.\n'
        child = subprocess.run(
            args=command, text=True, timeout=30.0, capture_output=True
        )
        child_exit_code = child.returncode
        child_stdout = child.stdout
        child_stderr = child.stderr
        if child_exit_code:
            output_string += f"Process exited with code {child_exit_code}.\n"
        if child_stdout:
            output_string += f"STDOUT: {child_stdout}.\n"
        if child_stderr:
            output_string += f"STDERR: {child_stderr}."
        return output_string
    except Exception as e:
        return f"Error: executing Python file: {e}."
