.PHONY: help install test lint build run benchmark-loc clean

PYTHON ?= python
NPM ?= npm

help:
	@echo "HealthPulse AI — Enterprise Healthcare Platform Build Orchestrator"
	@echo "Targets:"
	@echo "  install        Install Python and TypeScript dependencies"
	@echo "  test           Execute automated pytest test suite"
	@echo "  lint           Run code linters and type checkers"
	@echo "  build          Build frontend and container assets"
	@echo "  run            Launch unified server (FastAPI + Web Studio)"
	@echo "  benchmark-loc  Verify production LOC volume benchmark"
	@echo "  clean          Clean build artifacts and caches"

install:
	$(PYTHON) -m pip install -r requirements.txt || true
	$(NPM) install

test:
	$(PYTHON) -m pytest backend/tests/ -v

lint:
	$(PYTHON) -m flake8 backend/ sdk/ workers/ || true
	$(NPM) run lint --workspaces || true

build:
	$(NPM) run build --workspaces || true

run:
	$(PYTHON) run.py

benchmark-loc:
	@echo "Calculating production LOC benchmark..."
	@powershell -Command "Get-ChildItem -Recurse -File -Include *.py,*.ts,*.tsx,*.js,*.mjs -Exclude node_modules,.git,tests,*test*,package-lock.json,*.lock,data_storage,coverage,dist | Get-Content | Measure-Object -Line"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf dist build .next coverage 2>/dev/null || true
