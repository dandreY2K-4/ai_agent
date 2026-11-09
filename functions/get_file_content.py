import os

from ..config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
    if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory.'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    with open(target_file, "r") as f:
        try:
            content = f.read()
            if len(content) <= MAX_CHARS:
                return f"{content}"
            else:
                return f"{content[:MAX_CHARS]}\n...File {file_path} truncated: True at {MAX_CHARS} characters."
        except Exception as e:
            return f"Error: {e}"
