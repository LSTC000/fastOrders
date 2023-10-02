#!/bin/bash

alembic upgrade head

gunicorn app:create_app --workers=2 --worker-class=uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000