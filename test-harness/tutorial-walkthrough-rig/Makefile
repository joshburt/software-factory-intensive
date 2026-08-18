.DEFAULT_GOAL := help

VENV_DIR ?= .venv
UV := uv

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install dependencies
	$(UV) sync

.PHONY: test
test: ## Run tests
	$(UV) run pytest

.PHONY: lint
lint: ## Lint with ruff
	$(UV) run ruff check src/ tests/

.PHONY: format
format: ## Format with black and isort
	$(UV) run black src/ tests/
	$(UV) run isort src/ tests/

.PHONY: typecheck
typecheck: ## Type-check with mypy
	$(UV) run mypy src/ tests/