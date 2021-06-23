
from brownie import *


def main():
    ConvertLib.deploy({'from': accounts[0]})
    MetaCoin.deploy({'from': accounts[0]})
