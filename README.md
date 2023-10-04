![Python](https://img.shields.io/badge/Python-3.11.4-_)
![FastApi](https://img.shields.io/badge/FastApi-0.103.1-orange)
![Redis](https://img.shields.io/badge/Redis-7.2-red)
![Alembic](https://img.shields.io/badge/Alembic-1.12.0-red)
![SqlAlchemy](https://img.shields.io/badge/SqlAlchemy-2.0.21-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Docker](https://img.shields.io/badge/Docker-24.0.6-blue)


# Тестовое задание о курьерах и заказах от [*Estesis.tech*](https://estesis.tech)


### Инструкция по запуску:
1) Склонируйте репозиторий: 
    ``` 
    git clone https://github.com/LSTC000/fastOrders.git
    ```
2) Запустите проект одним из удобных способов:
    > ## **Ручной запуск**
    > + Установите необходимые сервисы: **[Redis](https://redis.io/docs/getting-started/installation/)**, **[PostgreSQL](https://www.postgresql.org/docs/current/tutorial-install.html)**.
    > + Создайте и активируйте виртуальное окружение:
    >   ```
    >   python -m venv venv
    >   ```
    >   ```
    >   .\venv\Scripts\activate
    >   ```
    > + Установите необходимые зависимости из requirements.txt в виртуальное окружение:
    >   ```
    >   pip install -r ./requirements.txt
    >   ```
    > + Создайте файл **.env** на основе файла **.env.dist**:
    >   ```
    >   ORIGINS=http://localhost:7777,
    >
    >   REDIS_HOST=your-redis-host
    >   REDIS_PORT=your-redis-port
    >
    >   DB_USER=your-db-username
    >   DB_PASS=your-db-password
    >   DB_HOST=your-db-host
    >   DB_PORT=your-db-port
    >   DB_NAME=your-db-name
    >   ```
    >   Origins - список источников, которым вы разрешаете использовать ваш API.
    > + Подключите миграции с помощью Alembic:
    >   ```
    >    alembic upgrade head
    >    ```
    > + Запустите веб-сервер Uvicorn с API:
    >   + Если у вас установлена утилита **make**, то вы можете воспользоваться командой из **Makefile**:
    >     ```
    >     make app-start
    >     ```
    >   + В противном случае выполните команду:
    >     ```
    >     uvicorn --factory app:create_app --workers=2 --reload --host=localhost --port=8000
    >     ```

    > ## **Docker запуск**
    >   + Окружающая среда для Docker находится в файле **.env.docker**. При желании её можно настроить под себя, но по умолчанию она уже имеет рабочую конфигурацию:
    >     ```
    >     ORIGINS=http://localhost:7777,
    >     REDIS_HOST=redis
    >     REDIS_PORT=6379
    >
    >     DB_USER=postgres
    >     DB_PASS=postgres
    >     DB_HOST=db
    >     DB_PORT=5432
    >     DB_NAME=postgres
    >     
    >     POSTGRES_USER=postgres
    >     POSTGRES_PASSWORD=postgres
    >     POSTGRES_DB=postgres
    >     ```
    >     При изменении **.env.docker** будте аккуратны с ***хостами*** и ***портами***. Следите, чтобы они совпадали с соответствующими ***хостами*** и ***портами*** сервисов в **docker-compose.yml**.
    >   + Далее следуйте инструкциям по запуску и управлению **docker-compose** в зависимости от того, есть ли у вас установленная утилита **make** или нет.
    >   + <span style="color:#E0303E">**Важно:**</span> Иногда при первом запуске контейнера **app** миграции **alembic** могут не подгрузиться в БД, поэтому, если при тестировании API 
          возникнут ошибки, связанные с работой БД, то просто ***остановите*** контейнеры: `make docker-stop` или `docker-compose stop`,
          а после заново ***запустите*** их: `make docker-start` или `docker-compose start`. Лично я рекомендую после команды `make docker-up` или `docker-compose up -d` (см. пункты ниже)
          сразу совершить остановку и запуск контейнеров, как это описано выше. Тогда никаких проблем с миграциями не будет.
    >     + ### Запуск Docker с make:
    >       + Команды для ***запуска*** docker-compose:
    >         + Сборка образов: 
    >           ```
    >           make docker-build
    >           ```
    >         + Запуск всех контейнеров:
    >           ```
    >           make docker-up
    >           ```
    >       + Команды для ***управления*** docker-compose          
    >         + Просмотр логов: `make docker-logs`
    >         + Остановка всех контейнеров: `make docker-stop`
    >         + Запуск всех остановленных контейнеров: `make docker-start`
    >         + Остановка и удаление всех контейнеров (без удаления томов): `make docker-down`
    >         + Остановка и удаление всех контейнеров (с удалением томов): `make docker-down-v`
    >     + ### Запуск Docker без make:
    >       + Команды для ***запуска*** docker-compose:
    >         + Сборка образов:
    >           ```
    >           docker-compose build
    >           ```
    >         + Запуск всех контейнеров:
    >           ```
    >           docker-compose up -d
    >           ```
    >       + Команды для ***управления*** docker-compose          
    >         + Просмотр логов: `docker-compose logs -f`
    >         + Остановка всех контейнеров: `docker-compose stop`
    >         + Запуск всех остановленных контейнеров: `docker-compose start`
    >         + Остановка и удаление всех контейнеров (без удаления томов): `docker-compose down`
    >         + Остановка и удаление всех контейнеров (с удалением томов): `docker-compose down -v`