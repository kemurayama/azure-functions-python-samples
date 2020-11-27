import os
import json

from flask import Flask
import requests

import logging

app = Flask(__name__)


def get_token():
    IDENTITY_ENDPOINT = os.environ.get('IDENTITY_ENDPOINT')
    IDENTITY_HEADER = os.environ.get('IDENTITY_HEADER')
    TARGET_APP = os.environ.get('FUNCTIONAPP_ID')

    headers = {
        "X-IDENTITY-HEADER": IDENTITY_HEADER
    }

    query = {
        "resource": TARGET_APP,
        "api-version": "2019-08-01"
    }

    r = requests.get(IDENTITY_ENDPOINT, params=query, headers=headers)
    response = r.json()

    return response


@app.route('/')
def hello_world():
    token_dict = get_token()

    return json.dumps(token_dict)


@app.route('/request_function')
def request_function():
    token_dict = get_token()

    FUNCTION_URL = os.environ.get('FUNCTION_URL')
    token = token_dict['access_token']

    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        r = requests.get(FUNCTION_URL, headers=headers)
        response = r.text
    except Exception as e:
        logging.exception(f'{e}')
        return e
        
    return response

@app.route('/get_sub')
def get_subscription():
    return os.environ.get('SUBSCRIPTION_ID')