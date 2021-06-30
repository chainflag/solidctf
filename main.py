#!/usr/bin/env python3
from menu import Menu


menu: Menu = Menu()
print(menu)

choice: int = int(input("[-]input your choice: "))
menu.select_option(choice)
