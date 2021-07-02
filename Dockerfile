FROM python:3-slim-buster
ENV PORT=20000
WORKDIR /opt

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential libsodium-dev tini xinetd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN brownie compile
RUN mkdir /var/log/ctf
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["tini", "-g", "--"]
CMD ["./entrypoint.sh"]
