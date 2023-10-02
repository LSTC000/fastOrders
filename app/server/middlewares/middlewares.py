from app.common import config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


class Middlewares:
    @staticmethod
    def register_cors(app: FastAPI):
        app.add_middleware(
            CORSMiddleware,
            allow_origins=config.origins,
            allow_credentials=True,
            allow_methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
            allow_headers=[
                'Content-Type',
                'Set-Cookie',
                'Access-Control-Allow-Headers',
                'Access-Control-Allow-Methods',
                'Access-Control-Allow-Origin',
                'Authorization'
            ],
        )
