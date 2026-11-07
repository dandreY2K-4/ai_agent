from functions.get_files_info import get_files_info

params = [
    (
        "calculator",
        ".",
        "Result for current directory:\n  - main.py: file_size=719 bytes, is_dir=False\n  - tests.py: file_size=1331 bytes, is_dir=False\n  - pkg: file_size=44 bytes, is_dir=True",
    ),
    (
        "calculator",
        "pkg",
        "Result for 'pkg' directory:\n  - calculator.py: file_size=1721 bytes, is_dir=False\n  - render.py: file_size=376 bytes, is_dir=False",
    ),
    (
        "calculator",
        "/bin",
        'Result for \'/bin\' directory:\n    Error: Cannot list "bin" as it is outside the permitted working directory',
    ),
    (
        "calculator",
        "../",
        'Error: Cannot list "../" as it is outside the permitted working directory',
    ),
]


def test(params) -> None | str:
    print("========== TESTS ==========\n")
    try:
        for i in range(len(params)):
            expected = params[i][2]
            actual = get_files_info(params[i][0], params[i][1])
            print(f"---------- Test {i+1} ----------")
            print("expected=\n", expected)
            print("actual=\n", actual)
        return
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    test(params=params)
