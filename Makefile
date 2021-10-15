lint:
	black --check . --diff
	flake8 --ignore=E501,W503 --show-source
	isort --profile black . --check --diff

format:
	black .
	isort --profile black .
