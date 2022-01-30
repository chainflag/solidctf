#!/usr/bin/env python3
import os

from run import conn_handler

os.environ["TOKEN_SECRET"] = "secret"
os.environ["WEB3_PROVIDER_URI"] = "http://localhost:8545"
os.system("cd example && brownie compile")

conn_handler("example")
