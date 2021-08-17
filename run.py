#!/usr/bin/env python3
import os

from eth_challenge_base.menu import Menu
from eth_challenge_base.config import parse_config
from eth_challenge_base.utils import Paseto, Build

if __name__ == '__main__':
    config = parse_config(os.path.join(os.path.dirname(__file__), "challenge.yml"))
    auth = Paseto(config.secret, exp_seconds=config.exp_seconds)
    build = Build(os.path.dirname(__file__))

    menu = Menu(auth, build, config)
    print(menu)

    choice = int(input("[-]input your choice: "))
    menu.select_option(choice)
