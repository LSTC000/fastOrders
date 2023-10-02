from .server import Server

from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title='Template')

    return Server(app).get_app()
