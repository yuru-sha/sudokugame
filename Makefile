.PHONY: help install clean test run lint format build

help:  ## Show this help message
	@echo 'Usage:'
	@echo '  make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install:  ## Install project dependencies
	poetry install

update:  ## Update dependencies to their latest versions
	poetry update

clean:  ## Remove build artifacts and cache directories
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	poetry env remove --all

test:  ## Run tests
	poetry run pytest tests/

run:  ## Run the game
	poetry run python -m src.sudokugame

lint:  ## Check code style
	poetry run ruff check .
	poetry run mypy src/

format:  ## Format code
	poetry run ruff format .

build:  ## Build the project
	poetry build

shell:  ## Spawn a shell within the virtual environment
	poetry shell 