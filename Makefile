.PHONY: dev prod down superuser

DEV_ENV = -f docker-compose.yml -f docker-compose.dev.yml
PROD_ENV = -f docker-compose.yml

prod:
	docker compose $(PROD_ENV) up -d --build

dev:
	docker compose $(DEV_ENV) up -d --build

superuser:
	docker compose $(PROD_ENV) exec web python src/manage.py createsuperuser

down:
	docker compose $(PROD_ENV) down

lint:
	docker compose $(DEV_ENV) exec web black .
	docker compose $(DEV_ENV) exec web ruff check . --fix

mm:
	docker compose $(DEV_ENV) exec web python src/manage.py makemigrations

migrate:
	docker compose $(DEV_ENV) exec web python src/manage.py migrate