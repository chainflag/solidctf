#!/bin/bash

read -r -d '' COMPILE <<-'EOF'
from brownie import project
from solcx import install

install.BINARY_DOWNLOAD_BASE = "https://cdn.jsdelivr.net/gh/ethereum/solc-bin@latest/{}-amd64/{}"
project.load(".")
EOF

if ! python3 -c "$COMPILE"; then
  exit 1
fi

gunicorn server:app \
  --bind "${HTTP_HOST:-127.0.0.1}":8000 \
  --daemon \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --access-logfile /var/log/ctf/gunicorn.access.log \
  --capture-output

source /xinetd.sh
