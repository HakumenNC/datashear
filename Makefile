# Makefile for DataShear package

.PHONY: help install install-dev test test-cov lint format clean build upload

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install package
	pip install .

install-dev:  ## Install package in development mode with dev dependencies
	pip install -e ".[dev]"

test:  ## Run tests
	pytest

test-cov:  ## Run tests with coverage
	pytest --cov=src --cov-report=html --cov-report=term

lint:  ## Run linting tools
	flake8 src tests
	mypy src

format:  ## Format code
	black src tests
	isort src tests

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build:  ## Build package
	python -m build

upload:  ## Upload to PyPI (requires authentication)
	python -m twine upload dist/*

upload-test:  ## Upload to TestPyPI (requires authentication)
	python -m twine upload --repository testpypi dist/*