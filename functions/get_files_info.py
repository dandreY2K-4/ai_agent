import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        output = (
            f"Result for '{directory}' directory:\n"
            if directory != "."
            else f"Result for current directory:\n"
        )
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))
        if not os.path.isdir(target_dir):
            output += f"    Error: '{directory}' is not a directory.\n"
        elif os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
            output += f'    Error: Cannot list "{directory}" as it is outside the permitted working directory.\n'
        else:
            dir_content = os.listdir(target_dir)
            for i in dir_content:
                abs_i_path = os.path.join(target_dir, i)
                file_size = os.path.getsize(abs_i_path)
                is_dir = os.path.isdir(abs_i_path)
                output += f"  - {i}: {file_size=} bytes, {is_dir=}.\n"
        return output

    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    print(get_files_info("functions", "."))
