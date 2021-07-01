FROM python:3-slim-buster

ENV PORT=20000
WORKDIR /home/ctf

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential xinetd tini \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m ctf \
    && mkdir /var/log/ctf

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
COPY ./ctf.xinetd /etc/xinetd.d/ctf

RUN chmod +x ./start.sh
RUN cd challenge && brownie compile --all && cd ../

ENTRYPOINT ["tini", "-g", "--"]
CMD ["./start.sh"]
