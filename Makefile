.PHONY: help
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

pip: ## Install python dependencies
	@echo "Installing Python dependencies"
	@pip install -r requirements.txt

start_deps: ## Start project dependencies(Eg.: Zookeeper...)
	@echo "Trying to start zookeeper"
	@zkServer start
	@echo "Trying to start rabbit-mq"
	@rabbitmq-server &

setup_logs: ## Create log structres
	@mkdir -p logs
	@touch logs/create_database_worker.txt
	@touch logs/destroy_database_worker.txt
	@touch logs/database_rpc_service.txt

start_db_service: ## Start database service
	@echo "Trying to start database service"
	@source $$VIRTUALENVWRAPPER_SCRIPT; workon python_zk_lab; python src/database_service.py &

start_create_db_worker: ## Start create database worker
	@echo "Trying to start create database worker"
	@source $$VIRTUALENVWRAPPER_SCRIPT; workon python_zk_lab; python src/worker/create_database_worker.py &

start_destroy_db_worker: ## Start destroy database worker
	@echo "Trying to start destroy database worker"
	@source $$VIRTUALENVWRAPPER_SCRIPT; workon python_zk_lab; python src/worker/destroy_database_worker.py &

start_all: ## Start all dependencies
	@make setup_logs
	@make start_deps
	@make start_db_service
	@make start_create_db_worker
	@make start_destroy_db_worker

clean-pyc: ## remove temporary files
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +
