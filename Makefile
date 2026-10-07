.PHONY: up down logs test lint fmt agent

up:        ## Start Postgres + API
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f api

test:
	pytest -q

lint:
	ruff check .

fmt:
	ruff format .

agent:     ## Run the agent once against the local API
	python -m opswatch_agent.cli --config agent/config.yaml --once
