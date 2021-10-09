lint:
	black --check . --diff
	flake8 --ignore=E501 --show-source
	isort --profile black . --check --diff

format:
	black .
	isort --profile black .
