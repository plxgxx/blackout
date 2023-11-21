all: pre_commit

pre_commit:
		pre-commit run --all

test:
		python -m pytest

cov:
		python -m pytest --cov-report html --cov=bot tests/
