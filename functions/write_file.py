import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes down content to a file provided a valid relative path from the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the requested file, relative to working directory.",
                },
                "content": {
                    "type": "string",
                    "description": "The intended content to be written into the file_path.",
                },
            },
            "required": ["file_path"],
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str) -> str:
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
    if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
        return f'Error: Cannot write to "{target_file}" as it is outside the permitted working directory.'
    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{target_file}" as it is a directory.'
    try:
        head, _ = os.path.split(target_file)
        os.makedirs(head, exist_ok=True)
        with open(target_file, "w") as f:
            written_chars = f.write(content)
            return f'Successfully wrote to "{target_file}" ({written_chars} characters written).'
    except Exception as e:
        return f"Error: {e}"
