#!/usr/bin/env python3
import signal

from eth_challenge_base.ui import UserInterface

if __name__ == "__main__":
    signal.alarm(60)
    UserInterface().run()
