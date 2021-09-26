#!/usr/bin/env python3
import os

from binascii import unhexlify

from eth_challenge_base.action import ActionHandler
from eth_challenge_base.config import parse_config
from eth_challenge_base.utils import Paseto, Build


def main():
    challenge_dir = os.path.dirname(__file__)
    if os.getenv("DEBUG", False):
        challenge_dir = os.path.join(challenge_dir, "example")

    secret = unhexlify(os.getenv("TOKEN_SECRET").encode("ascii"))
    exp_seconds = int(os.getenv("TOKEN_EXP_SECONDS")) if os.getenv("TOKEN_EXP_SECONDS") else None
    auth = Paseto(secret, exp_seconds=exp_seconds)
    build = Build(challenge_dir)
    config = parse_config(os.path.join(challenge_dir, "challenge.yml"))
    print(config.banner)

    actions = ActionHandler(auth, build, config)
    for i, action in enumerate(actions):
        print(f"{i+1} - {action.name}")

    action = int(input("[-]action? ")) - 1
    if action < 0 or action >= len(actions):
        print("can you not")
        exit(1)
    exit(actions[action].handler())


if __name__ == '__main__':
    main()
