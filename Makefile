.PHONY: help install dev-setup format lint test clean docker-build docker-run docker-stop docker-logs docker-restart docker-clean

# Default target
help: ## Show this help message
	@echo "Vakanse Telegram Bot - Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Development commands
install: ## Install production dependencies
	pip install -r requirements.txt

dev-setup: ## Setup development environment
	@chmod +x scripts/dev-setup.sh
	./scripts/dev-setup.sh

format: ## Format code with black and isort
	black app/ tests/
	isort app/ tests/

lint: ## Run linting with flake8 and mypy
	flake8 app/ tests/
	mypy app/

test: ## Run tests with pytest
	pytest tests/ -v --cov=app --cov-report=term-missing

test-html: ## Run tests with HTML coverage report
	pytest tests/ -v --cov=app --cov-report=html
	@echo "Coverage report available at htmlcov/index.html"

clean: ## Clean up cache and temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete

# Docker commands
docker-build: ## Build Docker image
	docker-compose build

docker-run: ## Start application with Docker
	@chmod +x scripts/start.sh
	./scripts/start.sh

docker-stop: ## Stop Docker containers
	docker-compose down

docker-logs: ## Show Docker container logs
	docker-compose logs -f

docker-restart: ## Restart Docker containers
	@chmod +x scripts/start.sh
	./scripts/start.sh restart

docker-clean: ## Clean up Docker resources
	docker-compose down --volumes --remove-orphans
	docker system prune -f

# Production commands
prod-build: ## Build production Docker image
	docker build -t vakanse-bot:latest .

prod-run: ## Run production container
	docker run -d \
		--name vakanse-bot \
		-p 8000:8000 \
		--env-file .env \
		--restart unless-stopped \
		vakanse-bot:latest

prod-stop: ## Stop production container
	docker stop vakanse-bot
	docker rm vakanse-bot

# Quality checks
check: format lint test ## Run all quality checks

pre-commit: ## Install and run pre-commit hooks
	pre-commit install
	pre-commit run --all-files

# Utility commands
logs: ## Create logs directory
	mkdir -p logs

env-check: ## Check environment configuration
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found"; \
		echo "Please copy env.example to .env and configure it"; \
		exit 1; \
	fi
	@echo "Environment file found"

status: ## Show application status
	@echo "=== Application Status ==="
	@if command -v docker-compose >/dev/null 2>&1; then \
		docker-compose ps; \
	else \
		echo "Docker Compose not available"; \
	fi

# Development workflow
dev: dev-setup ## Complete development setup
	@echo "Development environment ready!"

# Production workflow
prod: env-check docker-build docker-run ## Complete production deployment
	@echo "Production deployment complete!"

# Quick start for new developers
quick-start: ## Quick start for new developers
	@echo "Setting up Vakanse Telegram Bot..."
	@make dev-setup
	@echo ""
	@echo "Next steps:"
	@echo "1. Edit .env file with your configuration"
	@echo "2. Run 'make docker-run' to start the application"
	@echo "3. Check logs with 'make docker-logs'"
