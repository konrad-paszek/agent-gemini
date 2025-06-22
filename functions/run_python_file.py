import os
import subprocess

def run_python_file(working_directory, file_path):
    x = file_path
    abs_path = os.path.abspath(working_directory)
    file_path = os.path.abspath(os.path.join(working_directory, file_path))
    stderr = ''
    stdout = ''
    if not file_path.startswith(abs_path):
        return f'Error: Cannot execute "{x}" as it is outside the permitted working directory'
    if not os.path.exists(file_path):
        return f'Error: File "{x}" not found.'
    if not file_path.endswith('.py'):
        return f'Error: "{x}" is not a Python file.'
    process = subprocess.run(args=['python', f'{file_path}'], timeout=30, capture_output=True)
    if process.stdout:
        stdout = 'STDOUT: ' + str(process.stdout) + '\n'
    if process.stderr:
        stderr = 'STDERR: ' + str(process.stderr) + '\n'
    code = process.returncode
    result = stdout + stderr
    if code != 0:
        result += '\n' + f"Process exited with code {code}"
    if result == '':
        return 'No output produces'
    return result
    