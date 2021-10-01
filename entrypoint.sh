#!/bin/bash

if ! brownie compile; then
  exit 1
fi

if [ -z "$TOKEN_SECRET" ]; then
  TOKEN_SECRET=$(cat /dev/urandom | base64 | head -c64)
  export TOKEN_SECRET
fi

source /xinetd.sh
