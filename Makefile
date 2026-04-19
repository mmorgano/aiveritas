PYTHON ?= $(shell if [ -x .venv/bin/python ]; then echo .venv/bin/python; else echo python3; fi)
PIP ?= $(PYTHON) -m pip
PYLINTHOME ?= .pylint.d

.PHONY: help bootstrap generate-samples install-dev install-hooks ensure-pylint lint test review-check check ci

install-dev:
	$(PIP) install -r requirements.txt -r requirements-dev.txt

bootstrap: install-dev install-hooks

generate-samples:
	$(PYTHON) scripts/generate_sample_data.py

install-hooks:
	bash scripts/install_git_hooks.sh

ensure-pylint:
	@$(PYTHON) -c "import importlib.util, sys; sys.exit(0 if importlib.util.find_spec('pylint') else 1)" || \
	(printf '%s\n' 'Missing development dependency: pylint' 'Run: make install-dev'; exit 1)

lint: ensure-pylint
	PYLINTHOME=$(PYLINTHOME) $(PYTHON) -m pylint src tests

test:
	$(PYTHON) -m pytest

review-check: lint test

check: lint test

ci: bootstrap generate-samples check

help:
	@printf '%s\n' \
	'Available targets:' \
	'  make bootstrap         Install dev dependencies and Git hooks' \
	'  make generate-samples  Generate synthetic CSV datasets' \
	'  make install-dev       Install runtime and development dependencies' \
	'  make install-hooks     Install the versioned pre-commit hook' \
	'  make lint              Run pylint on src and tests' \
	'  make test              Run pytest' \
	'  make review-check      Run lint and tests after writing or reviewing code' \
	'  make check             Run lint and tests' \
	'  make ci                Run bootstrap, sample generation, lint, and tests'
