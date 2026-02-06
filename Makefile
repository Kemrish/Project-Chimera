# Project Chimera standard commands

PYTHON ?= python
PIP ?= pip
IMAGE_NAME ?= project-chimera-dev

.PHONY: help install test lint typecheck format check docker-build docker-shell clean

help:
	@echo "Project Chimera - standard commands"
	@echo
	@echo "  install       Install project and test dependencies (pip install .[test])"
	@echo "  test          Run pytest test suite"
	@echo "  lint          Run code quality checks (reserved for future Python code)"
	@echo "  typecheck     Run static type checks (reserved for future Python code)"
	@echo "  format        Auto-format code (reserved for future Python code)"
	@echo "  check         Run all local verification steps (test + lint + typecheck)"
	@echo "  docker-build  Build development Docker image"
	@echo "  docker-shell  Start an interactive shell inside dev Docker image"
	@echo "  clean         Remove Python build artifacts"

install:
	$(PIP) install --upgrade pip
	$(PIP) install ".[test]"

test:
	$(PYTHON) -m pytest

lint:
	@echo "lint: no runtime Python package yet; hook in ruff/flake8 when code is added."

typecheck:
	@echo "typecheck: no runtime Python package yet; hook in mypy/pyright when code is added."

format:
	@echo "format: no runtime Python package yet; hook in black/isort when code is added."

check: test lint typecheck

docker-build:
	docker build -t $(IMAGE_NAME) .

docker-shell: docker-build
	docker run --rm -it -v $$(pwd):/app $(IMAGE_NAME) /bin/bash

clean:
	rm -rf .pytest_cache .mypy_cache
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +
	find . -name "*.pyc" -delete -o -name "*.pyo" -delete

