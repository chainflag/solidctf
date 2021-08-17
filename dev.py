#!/usr/bin/env python3
import os
import secrets

from run import main


os.environ["TOKEN_SECRET"] = secrets.token_hex(32)
os.environ["WEB3_PROVIDER_URI"] = "http://localhost:8545"
os.system("cd challenge && brownie compile")

main()
