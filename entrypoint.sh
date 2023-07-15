#!/bin/bash

if ! python3 -c "from brownie import project; project.load('.')"; then
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
