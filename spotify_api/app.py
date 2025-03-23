from fastapi import FastAPI

app = FastAPI(title='Karoake Project')


@app.get('/')
def first_app():
    return {'message': 'Hello World!'}
