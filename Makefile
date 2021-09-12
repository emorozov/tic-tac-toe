.DEFAULT_GOAL := help

.PHONY: help
help:  ## List of all defined commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: lint
lint: ## Run linters on the repository
	flake8
	mypy .


.PHONY: test
test: ## Run unit tests in docker
	docker-compose \
	    -f deploy/docker-compose.yml \
	    --project-directory . \
	    run --rm --service-ports tictactoe-api /app/start-autotests.sh


.PHONY: runserver
runserver: ## Run Django server in docker
	docker-compose \
	    -f deploy/docker-compose.yml \
	    --project-directory . \
	    run --rm --service-ports tictactoe-api /app/start-django-dev.sh
