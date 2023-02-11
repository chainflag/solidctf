dev:
	cd example && brownie compile
	APP_ENV=development uvicorn server:app --reload

protoc:
	docker build --target protoc -t protoc --platform linux/amd64 .
	docker run --name protoc protoc
	docker cp protoc:/protobuf/generated eth_challenge_base && docker rm protoc

lint:
	black --check . --diff
	flake8 --ignore=E501,W503 --show-source
	isort --profile black . --check --diff

format:
	black .
	isort --profile black .

