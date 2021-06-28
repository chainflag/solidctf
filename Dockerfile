FROM python:3-slim-buster

WORKDIR /opt

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    xinetd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
COPY ./ctf.xinetd /etc/xinetd.d/ctf

RUN chmod +x ./start.sh
RUN cd challenge && brownie compile --all && cd ../

EXPOSE 20000

CMD ["/opt/start.sh"]
