from functions.get_files_info import get_files_info

params = [
    ("calculator", ".", 'Success: "." is within the working directory'),
    (
        "calculator",
        "/bin",
        'Error: Cannot list "/bin" as it is outside the permitted working directory',
    ),
    (
        "calculator",
        "../",
        'Error: Cannot list "../" as it is outside the permitted working directory',
    ),
    ("calculator", "main.py", 'Error: "main.py" is not a directory'),
]


def test(params) -> int:
    result = (len(params)) - 1
    print("=====TESTS=====")
    try:
        for i in range(result + 1):
            expected = params[i][2]
            actual = get_files_info(params[i][0], params[i][1])
            compare = expected == actual
            flag = "PASSED" if compare else "FAILED"
            print(f"Test {i+1}: {flag}")
            if compare:
                print(f"{(expected==actual)=}")
                print(actual, "\n")
                result -= 1
            else:
                print(f"{expected=}")
                print(f"{actual=}\n")
        return result
    except Exception as e:
        print(e)
        return result


if __name__ == "__main__":
    test(params=params)
