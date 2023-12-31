DC=docker-compose

.PHONY: app
app-start:
	uvicorn --factory app:create_app --workers=2 --reload --host=localhost --port=8000

.PHONY: docker
docker-build:
	$(DC) build
docker-up:
	$(DC) up -d
docker-stop:
	$(DC) stop
docker-start:
	$(DC) start
docker-down:
	$(DC) down
docker-down-v:
	$(DC) down -v
docker-logs:
	$(DC) logs -f
