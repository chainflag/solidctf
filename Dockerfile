FROM golang:1.20-buster as protoc

WORKDIR /protobuf-builder

COPY solidctf/protobuf protobuf
COPY solidctf/front-end/bundle protobuf

RUN apt update \
    && apt install unzip \
    && go install github.com/verloop/twirpy/protoc-gen-twirpy@latest \
    && wget https://github.com/protocolbuffers/protobuf/releases/download/v3.19.5/protoc-3.19.5-linux-x86_64.zip \
    && unzip protoc-3.19.5-linux-x86_64.zip \
    && cp bin/protoc /bin/protoc \
    && protoc --python_out=. --twirpy_out=. protobuf/challenge.proto
    && wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash \
    && nvm install node \
    && npm install webpack webpack-cli -g \
    && cd protobuf \
    && npm install twirpscript \
    && npx twirpscript \
    && wepack

FROM python:3.10-slim-buster

WORKDIR /ctf

RUN apt update \
    && apt install -y --no-install-recommends build-essential tini nginx \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY server.py .
COPY solidctf solidctf
COPY example/contracts contracts
COPY example/challenge.yml challenge.yml
COPY --from=protoc /protobuf-builder/protobuf solidctf/protobuf

COPY default /etc/nginx/sites-available/
COPY entrypoint.sh /entrypoint.sh
RUN mkdir /var/log/ctf
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["tini", "-g", "--"]
CMD ["/entrypoint.sh"]
