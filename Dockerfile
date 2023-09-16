FROM golang:1.20-buster as protoc

WORKDIR /protobuf-build

RUN apt update && apt install unzip
RUN go install github.com/verloop/twirpy/protoc-gen-twirpy@latest
RUN wget https://github.com/protocolbuffers/protobuf/releases/download/v3.19.5/protoc-3.19.5-linux-x86_64.zip && unzip protoc-3.19.5-linux-x86_64.zip && cp bin/protoc /bin/protoc

COPY solidctf/protobuf protobuf
RUN protoc --python_out=. --twirpy_out=. protobuf/challenge.proto

FROM node:lts-alpine as frontend

WORKDIR /frontend-build

COPY web/package.json web/yarn.lock ./
RUN yarn install

COPY web ./
COPY solidctf/protobuf/challenge.proto .

RUN apk add --no-cache protoc
RUN yarn protoc && yarn build

FROM python:3.9-slim-buster

WORKDIR /ctf

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY server.py .
COPY solidctf solidctf
COPY example/contracts contracts
COPY example/challenge.yml challenge.yml

COPY --from=protoc /protobuf-build/protobuf solidctf/protobuf
COPY --from=frontend /frontend-build/src web/src

COPY entrypoint.sh /entrypoint.sh
RUN mkdir /var/log/ctf
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
