import json
import os

import settings
from exceptions import AlaudaInputError


def get_api_endpoint(cloud):
    return settings.API_ENDPOINTS[cloud]


def save_token(api_endpoint, token):
    auth = {
        "token": token
    }
    config = {
        api_endpoint: auth
    }
    with open(settings.ALAUDACFG, 'w') as f:
        json.dump(config, f, indent=2)


def load_token():
    try:
        with open(settings.ALAUDACFG, 'r') as f:
            config = json.load(f)
            api_endpoint = config.keys()[0]
            token = config[api_endpoint]['token']
            return api_endpoint, token
    except:
        raise AlaudaInputError('Please login first')


def delete_token():
    try:
        os.remove(settings.ALAUDACFG)
    except:
        print '[alauda] Already logged out'


def build_headers(token):
    headers = {
        'Authorization': 'Token ' + token,
        'Content-type': 'application/json'
    }
    return headers
