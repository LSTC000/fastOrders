from .middlewares import __middlewares__
from .events import on_startup, on_shutdown
from .routers import __routers__

from fastapi import FastAPI


class Server:
    __app: FastAPI

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__register_middlewares(app)
        self.__register_events(app)
        self.__register_routers(app)

    def get_app(self) -> FastAPI:
        return self.__app

    @staticmethod
    def __register_middlewares(app):
        __middlewares__.register_cors(app)

    @staticmethod
    def __register_events(app):
        app.on_event('startup')(on_startup)
        app.on_event('shutdown')(on_shutdown)

    @staticmethod
    def __register_routers(app):
        __routers__.register_routers(app)
