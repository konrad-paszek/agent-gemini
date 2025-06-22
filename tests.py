from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def test_get_files_info():
    files = run_python_file("calculator", "main.py")
    print(files)
    files = run_python_file("calculator", "tests.py")
    print(files)
    files = run_python_file("calculator", "../main.py")
    print(files)
    files = run_python_file("calculator", "nonexistent.py")
    print(files)


if __name__ == '__main__':
    test_get_files_info()