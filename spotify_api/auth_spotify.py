import base64
from os import getenv

import requests
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

CLIENT_SECRET = getenv('CLIENT_SECRET')
CLIENT_ID = getenv('ClIENT_ID')
GENIUS_CLIENT_ID = getenv('GENIUS_CLIENT_SECRET')
GENIUS_CLIENT_SECRET = getenv('GENIUS_CLIENT_SECRET')
GENIUS_TOKEN = getenv('GENIUS_TOKEN')


def get_token():
    auth_value = base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('utf-8')).decode(
        'utf-8'
    )
    auth_url = 'https://accounts.spotify.com/api/token'

    headers = {'Authorization': f'Basic {auth_value}'}
    data = {'grant_type': 'client_credentials'}
    response = requests.post(auth_url, headers=headers, data=data)

    try:
        body = response.json()
        token = body['access_token']
        return token
    except HTTPException as e:
        print(f'Erro ao obter token: {e}')
        return
