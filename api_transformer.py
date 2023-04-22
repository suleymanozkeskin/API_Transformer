import os
import re
import sys
import json
import shutil
import openai
import subprocess
from termcolor import cprint
from dotenv import load_dotenv
import fire

# Set up the OpenAI API
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL", "gpt-3.5-turbo")

with open("prompt.txt") as f:
    SYSTEM_PROMPT = f.read()

class FileExtensionError(ValueError):
    pass


def check_file_extension(output_framework, output_file):
    output_framework = output_framework.lower()
    if output_framework in ["express.js", "node.js"]:
        expected_extension = ".js"
    elif output_framework in ["fastapi", "flask", "django"]:
        expected_extension = ".py"
    else:
        raise ValueError("Unsupported target framework")

    if not output_file.endswith(expected_extension):
        raise FileExtensionError(
        f"The output file '{output_file}' has an incorrect extension for the {output_framework} framework. "
        f"Please provide a file with the expected extension '{expected_extension}'."
        )
    
        
    


def api_transformer(input_file, output_framework, output_file, model=DEFAULT_MODEL):
    check_file_extension(output_framework, output_file)

    # Read the input_file
    with open(input_file, "r") as f:
        file_content = f.read()

    # Prepare the prompt for GPT
    prompt = (
        "I have an API function written in one backend framework and I need your help to transform it to another framework.\n\n"
        "Here's the original API code:\n\n"
        "{}\n\n"
        "Please help me transform this code to {}.\n"
    ).format(file_content, output_framework)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    # Get the response from GPT
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.5,
    )

    transformed_code = response.choices[0].message.content.strip()

    # Write the transformed code to the output_file
    with open(output_file, "w") as f:
        f.write(transformed_code)

    print("API function transformed and saved in {}".format(output_file))
    print("Note:You may still need to do comment out from GPT's output as file includes comments from the prompt.")



def main():
    try:
        fire.Fire(api_transformer)
    except FileExtensionError as e:
        print(str(e))



if __name__ == "__main__":
    main()