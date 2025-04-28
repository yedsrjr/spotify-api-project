from http import HTTPStatus

from fastapi import FastAPI

from spotify_api.routers import auth, users
from spotify_api.schemas import Message

app = FastAPI(title='Karoake Project')

app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello World!'}
