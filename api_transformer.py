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


def api_transformer(input_file, output_framework, output_file, model=DEFAULT_MODEL):
    if not output_framework.lower() in ["express.js", "node.js", "fastapi", "flask", "django"]:
        raise ValueError("Unsupported target framework")

    # Read the input_file
    with open(input_file, "r") as f:
        file_content = f.read()

    # Prepare the prompt for GPT-4
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

    # Get the response from GPT-4
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


if __name__ == "__main__":
    fire.Fire(api_transformer)
