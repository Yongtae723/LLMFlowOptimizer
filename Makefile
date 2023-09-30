tune-with-debug:
	HYDRA_FULL_ERROR=1 poetry run python llmflowoptimizer/run.py

fix-lint-install:
	poetry add pre-commit
	poetry run pre-commit install

fix-lint:
	poetry run pre-commit run -a

test:
	poetry run pytest tests/
