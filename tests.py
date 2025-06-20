import unittest
from functions.get_files_info import get_files_info

def test_get_files_info():
    files = get_files_info('calculator', '.')
    print(files)
    files = get_files_info('calculator', 'pkg')
    print(files)
    files = get_files_info('calculator', '/bin')
    print(files)
    files = get_files_info('calculator', '../')
    print(files)


if __name__ == '__main__':
    test_get_files_info()