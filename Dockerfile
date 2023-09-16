FROM golang:1.20-buster as protoc

WORKDIR /protobuf-builder

RUN apt update && apt install unzip
RUN go install github.com/verloop/twirpy/protoc-gen-twirpy@latest
RUN wget https://github.com/protocolbuffers/protobuf/releases/download/v3.19.5/protoc-3.19.5-linux-x86_64.zip && unzip protoc-3.19.5-linux-x86_64.zip && cp bin/protoc /bin/protoc

COPY solidctf/protobuf protobuf
RUN protoc --python_out=. --twirpy_out=. protobuf/challenge.proto

FROM python:3.9-slim-buster

WORKDIR /ctf

RUN apt update \
    && apt install -y --no-install-recommends build-essential tini xinetd \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY client.py .
COPY server.py .
COPY solidctf solidctf
COPY example/contracts contracts
COPY example/challenge.yml challenge.yml
COPY --from=protoc /protobuf-builder/protobuf solidctf/protobuf

COPY xinetd.sh /xinetd.sh
COPY entrypoint.sh /entrypoint.sh
RUN mkdir /var/log/ctf
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["tini", "-g", "--"]
CMD ["/entrypoint.sh"]
