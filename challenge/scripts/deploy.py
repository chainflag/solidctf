from brownie import Greeter, accounts


def main():
    Greeter.deploy("HelloWorld", {'from': accounts[0]})
