import re
from http import HTTPStatus

from auth import GENIUS_TOKEN, get_token, requests
from bs4 import BeautifulSoup


def search_lyrics(query, access_token=GENIUS_TOKEN):
    url = 'https://api.genius.com/search'

    headers = {'Authorization': f'Bearer {access_token}'}

    params = {'q': query}

    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == HTTPStatus.OK:
        data = response.json()['response']['hits']
        if data:
            url_musica = data[0]['result']['url']
            return url_musica
    else:
        print(f'Erro: {response.status_code}')


def get_lyrics(url):
    response = requests.get(url)

    if response.status_code == HTTPStatus.OK:
        soup = BeautifulSoup(response.text, 'html.parser')
        letra = soup.find('div', class_='Lyrics__Container-sc-926d9e10-1 fEHzCI')
        texto = letra.get_text(separator='<br/>')
        texto = texto.replace('<br/>', '\n')
        texto = re.sub(r'(\[.*?\])', r'\n\1\n', texto)
        texto = re.sub(
            r'(?i)(You might also like.*?Embed.*?)(?=\n)', '', texto, flags=re.DOTALL
        )
        texto = re.sub(r'\n+', '\n', texto)

        return texto


# Altera limit para aumentar o número de músicas listadas


def search_track(query, access_token=get_token(), limit=1, market='BR'):
    url = 'https://api.spotify.com/v1/search'
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
        'q': query,
        'type': 'track',  # Buscando apenas faixas (músicas)
        'limit': limit,
        'market': market,
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    tracks = data.get('tracks', {}).get('items', [])
    if response.status_code == HTTPStatus.OK:
        data = response.json()

        tracks = data.get('tracks', {}).get('items', [])
        lista_musicas = []
        if tracks:
            for musica in tracks:
                pixel_img = 300
                music = musica['name']
                artista = ', '.join([artist['name'] for artist in musica['artists']])
                img = [
                    image['url']
                    for image in musica['album']['images']
                    if image['height'] == pixel_img
                ]
                album = musica['album']['name']
                url_letra = search_lyrics(f'{artista} {music}')
                letra = get_lyrics(url_letra)
                uri = musica['uri']
            lista_musicas.append({
                'musica': music,
                'artista': artista,
                'img': img,
                'letra': letra,
                'album': album,
                'uri': uri,
            })
            print(lista_musicas)
        else:
            print('Erro na busca:', response.status_code, response.text)


search_track('Até o Sol Raiar')
