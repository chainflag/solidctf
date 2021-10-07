FROM python:3.9.7-slim-buster

WORKDIR /home/ctf

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential tini xinetd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY run.py .
COPY example .
COPY eth_challenge_base eth_challenge_base

COPY xinetd.sh /xinetd.sh
COPY entrypoint.sh /entrypoint.sh
RUN mkdir /var/log/ctf
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["tini", "-g", "--"]
CMD ["/entrypoint.sh"]
