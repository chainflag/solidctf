#!/usr/bin/env python3
from core.account import Account
from core.build import Build
from core.contract import Contract

account = Account()
print(account.address)

build = Build("challenge")
contract = Contract(build.get("Greeter"))
print(contract.deploy.estimate_gas("HelloWorld"))

print(account.get_contract_address())
tx_hash = account.deploy(contract, "HelloWorld")
print(tx_hash)
