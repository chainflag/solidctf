FROM python:3-slim-buster

WORKDIR /home/ctf

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential libsodium-dev tini xinetd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY run.py .
COPY challenge .
COPY eth_challenge_base eth_challenge_base

COPY shell /startup
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["tini", "-g", "--"]
CMD ["/entrypoint.sh"]
