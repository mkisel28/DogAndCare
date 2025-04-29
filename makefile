COMPOSE_FILE=docker-compose.yml

WEB_SERVICE=web
CELERY1_SERVICE=celery1
CELERY2_SERVICE=celery2
FLOWER_SERVICE=flower

ENV_FILE=.env

DC=docker compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE)

.PHONY: help up down restart build logs shell migrate makemigrations collectstatic createsuperuser format lint

help:
	@echo "  make up               — Запуск всех контейнеров"
	@echo "  make down             — Остановка и удаление контейнеров"
	@echo "  make restart          — Перезапуск контейнеров"
	@echo "  make build            — Сборка образов"
	@echo "  make logs             — Логи веб-сервиса"
	@echo "  make shell            — Bash внутри веб-контейнера"
	@echo "  make migrate          — Применение миграций"
	@echo "  make makemigrations   — Создание миграций"
	@echo "  make collectstatic    — Сборка статики"
	@echo "  make createsuperuser  — Создание суперпользователя"
	@echo "  make format           — Форматирование (ruff)"
	@echo "  make lint             — Линтинг (ruff)"

up:
	$(DC) up -d

down:
	$(DC) down

restart:
	$(MAKE) down
	$(MAKE) up -d

build:
	$(DC) up -d --build

logs:
	$(DC) logs -f $(WEB_SERVICE)

shell:
	$(DC) exec $(WEB_SERVICE) bash

migrate:
	$(DC) exec $(WEB_SERVICE) python manage.py migrate

makemigrations:
	$(DC) exec $(WEB_SERVICE) python manage.py makemigrations

collectstatic:
	$(DC) exec $(WEB_SERVICE) python manage.py collectstatic --noinput

createsuperuser:
	$(DC) exec $(WEB_SERVICE) python manage.py createsuperuser

format:
	$(DC) exec $(WEB_SERVICE) ruff --fix .

lint:
	$(DC) exec $(WEB_SERVICE) ruff .
