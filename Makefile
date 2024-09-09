.PHONY: check install
check:
	pre-commit run --all-files

install:
	pip install -r ./requirements-dev.txt
	pre-commit install
