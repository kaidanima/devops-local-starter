SHELL := /bin/bash
# Prefer Docker Compose V2 plugin ("docker compose"); fall back to legacy docker-compose if V2 is unavailable
COMPOSE ?= $(shell if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then echo "docker compose"; elif command -v docker-compose >/dev/null 2>&1; then echo docker-compose; else echo "docker compose"; fi)

# Compose project/service names (used for image/container names)
PROJECT ?= devops-local-starter
SERVICE_API ?= api

export PYTHONPATH := .

.PHONY: help up down logs restart build rebuild test lint fmt scan gitleaks clean hooks init run alembic-rev alembic-upgrade alembic-downgrade psql print-compose doctor curl-health curl-users smoke wait

help:
	@echo "make init           - create venv and install requirements"
	@echo "make run            - run FastAPI locally (uvicorn)"
	@echo "make up             - docker compose up (detached, build)"
	@echo "make down           - docker compose down"
	@echo "make logs           - follow logs"
	@echo "make restart        - restart stack"
	@echo "make build          - compose build"
	@echo "make rebuild        - compose build --no-cache"
	@echo "make test           - run pytest"
	@echo "make lint           - flake8 + black --check + isort --check + bandit"
	@echo "make fmt            - auto-format (black + isort)"
	@echo "make alembic-rev    - alembic revision --autogenerate"
	@echo "make alembic-upgrade- upgrade head"
	@echo "make alembic-downgrade- downgrade -1"
	@echo "make psql           - connect to local postgres (host: localhost)"
	@echo "make scan           - Trivy image scan"
	@echo "make gitleaks       - scan repo for secrets"
	@echo "make clean          - down -v + prune images/volumes"
	@echo "make hooks          - install pre-commit hooks"
	@echo "make print-compose  - show which compose CLI will be used"
	@echo "make doctor         - diagnose compose setup and validate config"
	@echo "make curl-health    - curl http://127.0.0.1:8080/health"
	@echo "make curl-users     - curl http://127.0.0.1:8080/users/"
	@echo "make wait           - wait until http://127.0.0.1:8080/health returns 200"
	@echo "make smoke          - wait then curl both endpoints as a quick smoke test"

init:
	python3 -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

run:
	. .venv/bin/activate && uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

up:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f --tail=200

restart: down up

build:
	$(COMPOSE) build

rebuild:
	$(COMPOSE) build --no-cache

test:
	. .venv/bin/activate && pytest -q

lint:
	. .venv/bin/activate && flake8 src && black --check src tests && isort --check-only src tests && bandit -r src

fmt:
	. .venv/bin/activate && black src tests && isort src tests

scan:
	@echo "Scanning API image with Trivy..."
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image $(PROJECT)-$(SERVICE_API) || true

gitleaks:
	docker run --rm -v $$PWD:/repo zricethezav/gitleaks:latest detect --no-git -s=/repo || true

clean:
	$(COMPOSE) down -v --remove-orphans
	docker image prune -f
	docker volume prune -f

hooks:
	. .venv/bin/activate && pre-commit install

print-compose:
	@echo Using COMPOSE='$(COMPOSE)'

doctor:
	@echo Using COMPOSE='$(COMPOSE)'
	-$(COMPOSE) version || true
	-$(COMPOSE) config -q || true

curl-health:
	@curl -sS -i http://127.0.0.1:8080/health

curl-users:
	@curl -sS -i http://127.0.0.1:8080/users/

wait:
	@echo "[wait] Phase 1: Waiting for API inside container (http://127.0.0.1:8000/health) ..."
	@retries=90; \
	until $(COMPOSE) exec -T $(SERVICE_API) sh -c 'curl -fsS http://127.0.0.1:8000/health >/dev/null 2>&1'; do \
	  retries=$$((retries-1)); \
	  if [ $$retries -le 0 ]; then echo "Timed out waiting for API (inside container)"; exit 1; fi; \
	  sleep 2; \
	done; \
	echo "[wait] API inside container is healthy."; \
	\
	echo "[wait] Phase 2: Waiting for Traefik route (http://127.0.0.1:8080/health) ..."; \
	res=60; \
	until curl -fsS http://127.0.0.1:8080/health >/dev/null 2>&1; do \
	  res=$$((res-1)); \
	  if [ $$res -le 0 ]; then echo "Timed out waiting for Traefik route"; exit 1; fi; \
	  sleep 2; \
	done; \
	echo "[wait] Traefik route is healthy."

smoke: wait curl-health
	@echo "\n---\n"
	$(MAKE) curl-users

alembic-rev:
	. .venv/bin/activate && alembic revision --autogenerate -m "init db"

alembic-upgrade:
	. .venv/bin/activate && alembic upgrade head

alembic-downgrade:
	. .venv/bin/activate && alembic downgrade -1

# Simple helper to connect to Postgres on localhost (requires psql installed)
psql:
	psql "postgresql://$${POSTGRES_USER:-appuser}:$${POSTGRES_PASSWORD:-secretpassword}@$${POSTGRES_HOST:-localhost}:$${POSTGRES_PORT:-5432}/$${POSTGRES_DB:-appdb}"