.PHONY: tests

all: down build up

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

view-db:
	docker-compose exec web-db psql -U postgres

integration-tests: up
	docker-compose exec web python -m pytest tests/integration

unit-tests: up
	docker-compose exec web python -m pytest tests/unit

e2e-tests: up
	docker-compose exec web python -m pytest tests/e2e

tests: integration-tests unit-tests e2e-tests