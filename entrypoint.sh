#!/bin/bash

read -r -d '' COMPILE <<- 'EOF'
from brownie import project
from solcx import install

install.BINARY_DOWNLOAD_BASE = "https://cdn.jsdelivr.net/gh/ethereum/solc-bin@latest/{}-amd64/{}"
project.load(".")
EOF


if ! python3 -c "$COMPILE"; then
  exit 1
fi

if [ -z "$TOKEN_SECRET" ]; then
  TOKEN_SECRET=$(cat /dev/urandom | base64 | head -c64)
  export TOKEN_SECRET
fi

source /xinetd.sh
