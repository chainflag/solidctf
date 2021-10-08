#!/usr/bin/env python3
import os
import signal
import sys

from eth_challenge_base import __version__
from eth_challenge_base.action import ActionHandler
from eth_challenge_base.config import parse_config
from eth_challenge_base.utils import Powser

signal.alarm(60)


def main():
    difficulty = int(os.getenv("POW_DIFFICULTY", '0'))
    if difficulty != 0:
        powserver = Powser(difficulty)
        print(powserver)
        if not powserver.verify_hash(input("[-] ??? = ")):
            print("[+] wrong proof")
            sys.exit(1)

    challenge_dir = os.path.dirname(__file__)
    if os.getenv("DEBUG", False):
        print("version:", __version__)
        challenge_dir = os.path.join(challenge_dir, "example")

    config = parse_config(os.path.join(challenge_dir, "challenge.yml"))
    print(config.description)
    actions = ActionHandler(challenge_dir, config)
    for i, action in enumerate(actions):
        print(f"[{i+1}] - {action.description}")

    choice = None
    while choice is None:
        try:
            choice = int(input("[-] input your choice: ")) - 1
        except ValueError:
            print("must be an integer")
            continue
        else:
            if choice < 0 or choice >= len(actions):
                print("invalid option")
                sys.exit(1)

    sys.exit(actions[choice].handler())


if __name__ == "__main__":
    main()
