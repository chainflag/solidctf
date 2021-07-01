#!/bin/bash

for f in "$(pwd)"/startup/*; do
    echo "[+] running $f"
    bash "$f"
done

tail -f /var/log/ctf/*
