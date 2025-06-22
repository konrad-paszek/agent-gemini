import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
import argparse

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

parser = argparse.ArgumentParser()
parser.add_argument("prompt", type=str)
parser.add_argument("--verbose", action='store_true')
args = parser.parse_args()
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
schema_get_file_content =  types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file in the specified directory (limited to the working directory). The content will be truncated if it becomes too long.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="It is reading a content from a file in the specified directory, constrained to the working directory, it will truncate after getting too long string",
            ),
        },
    ),
)
schema_run_python_file =  types.FunctionDeclaration(
    name="run_python_file",
    description="It executes a python file, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Executes a Python file, limited to the working directory.",
            ),
        },
    ),
)
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file, limited to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Target file path relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file.",
            ),
        },
    ),
)
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
try:
    prompt = args.prompt
except IndexError:
    print("prompt cannot be empty")
    sys.exit(code=1)
messages = types.Content(role="user", parts=[types.Part(text=prompt)])
response  = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
if args.verbose:
    print(args)
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
function_calls_part = response.function_calls
if function_calls_part:
    for function_call_part in function_calls_part:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
else:
    print(response.text)


