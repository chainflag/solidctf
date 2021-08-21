#!/bin/bash

if [ -z "$TOKEN_SECRET" ]; then
  TOKEN_SECRET=$(python -c "import secrets; print(secrets.token_hex(32))")
  export TOKEN_SECRET
fi

for f in /startup/*; do
    echo "[+] running $f"
    bash "$f"
done

tail -f /var/log/ctf/*
