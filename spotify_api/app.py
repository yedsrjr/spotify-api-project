from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from spotify_api.schemas import Message

app = FastAPI(title='Karoake Project')


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def hello_world():
    return {'message': 'Hello World!'}


@app.get('/ola-mundo', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def ola_mundo_hmtl():
    return """
        <html>
        <head>
        </head>
        <body>
            <h1>Olá Mundo</h1>
        </body>
        </html>
    """
