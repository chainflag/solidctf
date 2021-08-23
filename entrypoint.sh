#!/bin/bash

if ! brownie compile; then
  exit 1
fi

if [ -z "$TOKEN_SECRET" ]; then
  TOKEN_SECRET=$(python -c "import secrets; print(secrets.token_hex(32))")
  export TOKEN_SECRET
fi

source /xinetd.sh
