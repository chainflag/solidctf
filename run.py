#!/usr/bin/env python3
import os
import signal
import sys

from eth_challenge_base.action import Actions
from eth_challenge_base.config import parse_config
from eth_challenge_base.utils import Powser


def conn_handler(project_path: str = "."):
    signal.alarm(60)
    difficulty = int(os.getenv("POW_DIFFICULTY", "0"))
    if difficulty != 0:
        pow_challenge = Powser(difficulty)
        print(f"[+] {pow_challenge}")
        if not pow_challenge.verify_hash(input("[-] ??? = ")):
            print("[+] wrong proof")
            sys.exit(1)

    project_path = os.path.join(os.path.dirname(__file__), project_path)
    config = parse_config(os.path.join(project_path, "challenge.yml"))
    print(config.description)
    actions = Actions(project_path, config)
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
    conn_handler()
