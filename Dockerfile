FROM golang:1.20-buster as protoc
WORKDIR /protobuf-builder
COPY solidctf/protobuf protobuf
RUN sed -i "s|http://deb.debian.org/debian|http://mirror.sjtu.edu.cn/debian|g" /etc/apt/sources.list \
    && go env -w GO111MODULE=on && go env -w GOPROXY=https://goproxy.cn,direct \
    && apt update && apt install -y protobuf-compiler \
    && go install github.com/verloop/twirpy/protoc-gen-twirpy@latest \
    && protoc --python_out=. --twirpy_out=. protobuf/challenge.proto

FROM node:20-alpine3.17 as webpack
WORKDIR /app
COPY solidctf/front-end/bundle .
COPY solidctf/protobuf/challenge.proto .
RUN npm config set registry https://registry.npm.taobao.org \
    && npm install webpack webpack-cli -g && npm install twirpscript \
    && apk add protoc && npx twirpscript && webpack

FROM python:3.10-slim-buster
WORKDIR /ctf
COPY requirements.txt .
COPY server.py .
COPY solidctf solidctf
COPY challenge-example/contracts contracts
COPY challenge-example/challenge.yml challenge.yml
COPY --from=protoc /protobuf-builder/protobuf solidctf/protobuf
COPY --from=webpack /app/dist/bundle.js /www/var/html/bundle.js
COPY default /etc/nginx/sites-available/
COPY entrypoint.sh /entrypoint.sh
COPY ./solidctf/front-end/static /www/var/html

RUN sed -i "s|http://deb.debian.org/debian|http://mirror.sjtu.edu.cn/debian|g" /etc/apt/sources.list
RUN pip config set global.index-url https://mirror.sjtu.edu.cn/pypi/web/simple
RUN apt update
RUN apt install -y --no-install-recommends nginx
RUN pip install -r requirements.txt
RUN mkdir /var/log/ctf && chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
