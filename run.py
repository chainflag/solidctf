#!/usr/bin/env python3
import os
import signal

from eth_challenge_base.action import ActionHandler
from eth_challenge_base.config import parse_config
from eth_challenge_base.utils import Powser

signal.alarm(60)


def main():
    difficulty = int(os.getenv("POW_DIFFICULTY", '0'))
    if difficulty != 0:
        powserver = Powser(difficulty)
        print(f'''[+] sha256({ powserver.prefix } + ???).binary.endswith('{ '0' * powserver.difficulty }')''')
        answer: str = input('[-] ??? = ')
        if not powserver.verify_hash(answer):
            print('[+] wrong proof')
            exit(1)

    challenge_dir = os.path.dirname(__file__)
    if os.getenv("DEBUG", False):
        challenge_dir = os.path.join(challenge_dir, "example")

    config = parse_config(os.path.join(challenge_dir, "info.yaml"))
    print(config.description)
    actions = ActionHandler(os.path.join(challenge_dir, "build/contracts"), config)
    for i, action in enumerate(actions):
        print(f"{i+1} - {action.name}")

    choice = None
    while choice is None:
        try:
            choice = int(input("[-]input your choice: ")) - 1
        except ValueError:
            print("must be an integer")
            continue
        else:
            if choice < 0 or choice >= len(actions):
                print("invalid option")
                exit(1)

    exit(actions[choice].handler())


if __name__ == '__main__':
    main()
