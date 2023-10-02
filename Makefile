DC=docker-compose

.PHONY: app
app-start:
	uvicorn --factory app:create_app --workers=2 --reload --host=localhost --port=8000

.PHONY: docker
docker-build:
	$(DC) build
docker-start:
	$(DC) up -d
docker-stop:
	$(DC) stop
docker-down:
	$(DC) down
docker-down-v:
	$(DC) down -v
docker-logs:
	$(DC) logs -f

.PHONY: celery
celery:
	celery -A app.utils.celery.celery:send_log_celery worker --loglevel=INFO --pool=solo
flower:
	celery -A app.utils.celery.celery:send_log_celery flower