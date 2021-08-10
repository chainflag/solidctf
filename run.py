#!/usr/bin/env python3
import os

from base import _MenuBase
from config import parse_config, Config
from utils import Build, Paseto


class Menu(_MenuBase):
    def __init__(self, auth: Paseto, build: Build, config: Config) -> None:
        super().__init__(auth, build, config)


if __name__ == '__main__':
    config = parse_config(os.path.join(os.path.dirname(__file__), "config.yml"))
    auth = Paseto(config.secret, exp_seconds=config.exp_seconds)
    build = Build(os.path.dirname(__file__))

    menu = Menu(auth, build, config)
    print(menu)

    choice = int(input("[-]input your choice: "))
    menu.select_option(choice)
