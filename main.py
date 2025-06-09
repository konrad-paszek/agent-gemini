import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("prompt", type=str)
parser.add_argument("--verbose", action='store_true')
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
try:
    prompt = args.prompt
except IndexError:
    print("prompt cannot be empty")
    sys.exit(code=1)
messages = types.Content(role="user", parts=[types.Part(text=prompt)])
response  = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
if args.verbose:
    print(args)
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


print(response.text)


