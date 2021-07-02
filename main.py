#!/usr/bin/env python3
import os

from helper.auth import Paseto
from helper.build import Build
from menu.menu import Menu

secret: bytes = b'\xc0J\xaev\x84t\x8f"\x89\x0c3C\x1f\xa2\xe9+W\x9c\x85\xfe\x05G\xfe\x01\x91\x86\x0c\xef\xd7\xb5\xc6\xf0'

if __name__ == '__main__':
    auth: Paseto = Paseto(secret)
    build: Build = Build(os.path.dirname(__file__))

    menu: Menu = Menu(auth, build)
    print(menu)

    choice: int = int(input("[-]input your choice: "))
    menu.select_option(choice)
