FROM golang:1.20-buster as protoc

WORKDIR /protobuf

RUN apt update && apt install unzip
RUN go install github.com/verloop/twirpy/protoc-gen-twirpy@latest
RUN wget https://github.com/protocolbuffers/protobuf/releases/download/v3.19.5/protoc-3.19.5-linux-x86_64.zip && unzip protoc-3.19.5-linux-x86_64.zip && cp bin/protoc /bin/protoc

COPY eth_challenge_base/challenge.proto .
RUN mkdir generated && protoc --python_out=./generated --twirpy_out=./generated ./challenge.proto

FROM python:3.9-slim-buster

WORKDIR /home/ctf

RUN apt update \
    && apt install -y --no-install-recommends build-essential tini xinetd \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY run.py .
COPY server.py .
COPY example .
COPY eth_challenge_base eth_challenge_base
COPY --from=protoc /protobuf/generated eth_challenge_base/generated

COPY xinetd.sh /xinetd.sh
COPY entrypoint.sh /entrypoint.sh
RUN mkdir /var/log/ctf
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["tini", "-g", "--"]
CMD ["/entrypoint.sh"]
