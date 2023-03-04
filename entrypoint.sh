#!/bin/bash

read -r -d '' COMPILE <<-'EOF'
import os

from brownie import project
from solcx import install

default = os.getenv(
    "SOLC_DOWNLOAD_BASE", "https://cdn.jsdelivr.net/gh/ethereum/solc-bin@latest"
).rstrip("/")

install.BINARY_DOWNLOAD_BASE = default + "/{}-amd64/{}"
project.load(".")
EOF

if ! python3 -c "$COMPILE"; then
  exit 1
fi

gunicorn server:app \
  --bind "${HTTP_HOST:-127.0.0.1}":8000 \
  --daemon \
  --preload \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --access-logfile /var/log/ctf/gunicorn.access.log \
  --error-logfile /var/log/ctf/gunicorn.error.log \
  --capture-output

source /xinetd.sh
