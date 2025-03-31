.PHONY: help install update lint tangle process-sessions process-contacts process-knowledge clean

.DEFAULT_GOAL := help

# Colors for help output
YELLOW := \033[1;33m
GREEN := \033[1;32m
NC := \033[0m

## Show help for each of the Makefile targets
help:
	@echo "NLP Healthcare Summit 2025 - Build Targets"
	@echo "-----------------------------------------"
	@grep -E '^## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = "## "}; {printf "$(GREEN)%s$(NC)\n", $$2}'
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

## Setup the project environment
install: ## Install project dependencies
	poetry install

## Update repository content and generate outputs
update: ## Run all processing scripts
	./update.sh

## Lint Org mode files
lint: ## Lint all org files for issues
	./lint-org.sh

## Tangle all Org mode files
tangle: ## Extract source code from org files
	./tangle-org.sh

## Process specific data
process-sessions: ## Process session data
	poetry run process-sessions

## Process contact information
process-contacts: ## Process contact information
	poetry run process-contacts

## Process knowledge base
process-knowledge: ## Process knowledge base
	poetry run process-knowledge

## Clean generated files
clean: ## Remove generated files
	find docs -name "*.csv" -o -name "*.json" -o -name "*.png" -type f -delete
	@echo "Cleaned generated files"