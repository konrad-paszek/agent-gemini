import os

def get_files_info(working_directory, directory=None):
    if working_directory != directory and not directory in os.listdir(working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory{working_directory}'
    if not os.path.isdir(working_directory):
        return f'Error: "{directory}" is not a directory'
    result = ''
    for filename in os.listdir(working_directory):
        abs_path = os.path.abspath(os.path.join(working_directory, filename))
        is_dir = os.path.isdir(os.path.join(working_directory, filename))
        result += f'- {filename}: file_size={os.path.getsize(abs_path)} bytes, is_dir={is_dir}\n'
        if is_dir:
            result += get_files_info(os.path.abspath(os.path.join(working_directory, filename)), os.path.join(abs_path))
    return result

