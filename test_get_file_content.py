from functions.get_file_content import get_file_content

print("Test for 'calculator' and 'main.py':")
print(f"{(get_file_content("calculator", "main.py"))=}\n")
print("Test for 'calculator' and 'pkg/calculator.py':")
print(f"{(get_file_content("calculator", "pkg/calculator.py"))=}\n")
print("Test for 'calculator' and '/bin/cat':")
print(f"{(get_file_content("calculator", "/bin/cat"))=}\n")
print("Test for 'calculator' and 'pkg/does_not_exist.py':")
print(f"{(get_file_content("calculator", "pkg/does_not_exist.py"))=}\n")
print("Test for 'calculator' and 'lorem.txt':")
print(f"{(get_file_content("calculator", "lorem.txt"))=}\n")
