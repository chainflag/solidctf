#!/bin/bash

for f in "$(pwd)"/scripts/*; do
    echo "[+] running $f"
    bash "$f"
done

tail -f /var/log/ctf/*
