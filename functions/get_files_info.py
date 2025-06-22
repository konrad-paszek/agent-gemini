import os

def get_files_info(working_directory, directory=None):
    abs_path = os.path.abspath(working_directory)
    target_directory = abs_path
    if directory:
        target_directory = os.path.join(abs_path, directory)
    if not target_directory.startswith(abs_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(working_directory):
        return f'Error: "{directory}" is not a directory'
    result = ''
    for filename in os.listdir(target_directory):
        path = os.path.join(target_directory, filename)
        is_dir = os.path.isdir(path)
        result += f'- {filename}: file_size={os.path.getsize(path)} bytes, is_dir={is_dir}\n'
    return result

