#!/usr/bin/env python3
import os
import signal

from eth_challenge_base.action import ActionHandler
from eth_challenge_base.config import parse_config

signal.alarm(60)


def main():
    challenge_dir = os.path.dirname(__file__)
    if os.getenv("DEBUG", False):
        challenge_dir = os.path.join(challenge_dir, "example")

    config = parse_config(os.path.join(challenge_dir, "info.yaml"))
    print(config.description)
    actions = ActionHandler(os.path.join(challenge_dir, "build/contracts"), config)
    for i, action in enumerate(actions):
        print(f"{i+1} - {action.name}")

    choice = int(input("[-]input your choice: ")) - 1
    if choice < 0 or choice >= len(actions):
        print("can you not")
        exit(1)
    exit(actions[choice].handler())


if __name__ == '__main__':
    main()
