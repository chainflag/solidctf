#!/usr/bin/env python3
import os

from binascii import unhexlify

from eth_challenge_base.menu import Menu
from eth_challenge_base.config import parse_config
from eth_challenge_base.utils import Paseto, Build

if __name__ == '__main__':
    challenge_dir = os.path.dirname(__file__)
    if not os.getenv("DOCKER_RUNNING", False):  # for debug
        challenge_dir = os.path.join(challenge_dir, "challenge")

    secret = unhexlify(os.getenv("TOKEN_SECRET").encode("ascii"))
    exp_seconds = int(os.getenv("TOKEN_EXP_SECONDS")) if os.getenv("TOKEN_EXP_SECONDS") else None
    auth = Paseto(secret, exp_seconds=exp_seconds)
    build = Build(challenge_dir)
    config = parse_config(os.path.join(challenge_dir, "challenge.yml"))

    menu = Menu(auth, build, config)
    print(menu)

    choice = int(input("[-]input your choice: "))
    menu.select_option(choice)
