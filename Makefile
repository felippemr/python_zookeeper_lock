.PHONY: help
.DEFAULT_GOAL := help

pip: ## Install python dependencies
	@echo "Installing Python dependencies"
	@pip install -r requirements.txt

clean: # remove temporary files
	@find . -name \*.pyc -delete

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
