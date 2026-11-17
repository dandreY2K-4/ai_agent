import json

from collections.abc import Callable
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

available_functions = [
    schema_get_file_content,
    schema_get_files_info,
    schema_run_python_file,
    schema_write_file,
]


def call_function(tool_call, verbose: bool = False) -> dict:
    # The tool_call argument is one of the tool-call objects from message.tool_calls in main.py
    tool_message = {
        "role": "tool",
        "tool_call_id": tool_call.id,  # a unique ID for this call (we'll need it when we send the result back)
        "content": "",
    }
    function_name = tool_call.function.name  # the name of the function (a string)
    function_args = json.loads(
        tool_call.function.arguments or "{}"
    )  # the arguments, as a JSON string
    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    function_map: dict[str, Callable[..., str]] = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    if function_map.get(function_name):
        function_args["working_directory"] = "./calculator"
        result = function_map[function_name](**function_args)
        tool_message["content"] = result
    else:
        tool_message["content"] = f"Error: Unknown function: {function_name}"
    return tool_message
