#!/usr/bin/env python3
import os

from eth_challenge_base.action import ActionHandler
from eth_challenge_base.config import parse_config


def main():
    challenge_dir = os.path.dirname(__file__)
    if os.getenv("DEBUG", False):
        challenge_dir = os.path.join(challenge_dir, "example")

    config = parse_config(os.path.join(challenge_dir, "challenge.yml"))
    print(config.banner)
    actions = ActionHandler(config.flag, config.payable_value, challenge_dir)
    for i, action in enumerate(actions):
        print(f"{i+1} - {action.name}")

    choice = int(input("[-]action? ")) - 1
    if choice < 0 or choice >= len(actions):
        print("can you not")
        exit(1)
    exit(actions[choice].handler())


if __name__ == '__main__':
    main()
