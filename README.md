# Backend API Transformer

## About

You can transform your api's to following target frameworks: FastAPI, Flask, Django, Node.js and Express.js
Besides transforming existing api's , ChatGPT will suggest improvements as comments without changing original function.

## Setup

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cp .env.sample .env

Add your openAI api key to `.env`

_warning!_ By default wolverine uses gpt-3.5-turbo. If you wish to change it to gpt-4, simply change the variable `DEFAULT_MODEL` in `.env` to `gpt-4`

## Example Usage

See the appropriate format below:

api_transformer.py    “existing_script_to_transform.py”    “targeted_framework”  “targeted_script_name.py || targeted_script_name.js” 

To run with gpt-3.5-turbo (the default, tested option):

    python api_transformer.py user.py express.js user.js
    python api_transformer.py user.py django     user.js
