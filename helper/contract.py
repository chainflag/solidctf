#!/usr/bin/env python3
from typing import Dict, List, Optional, Tuple

from eth_typing import ChecksumAddress
from web3 import Web3, contract
from brownie.convert import Wei

from helper.account import Account


class Contract:
    def __init__(self, web3: Web3, build: Dict) -> None:
        self.web3 = web3
        self._build = build.copy()
        self.bytecode = build["bytecode"]
        self.deploy = ContractConstructor(self)

    @property
    def abi(self) -> List:
        return self._build["abi"]

    @property
    def name(self) -> str:
        return self._build["contractName"]

    def at(self, address: ChecksumAddress) -> contract.ContractFunctions:
        return self.web3.eth.contract(
            address=address,
            abi=self.abi
        ).functions


class ContractConstructor:
    def __init__(self, parent: "Contract") -> None:
        self._instance = parent.web3.eth.contract(
            abi=parent.abi,
            bytecode=parent.bytecode
        )

    def __call__(
            self,
            *args: Tuple,
            amount: int = 0,
            sender: Account,
            gas_limit: Optional[int] = None,
            gas_price: Optional[int] = None,
            nonce: Optional[int] = None,
    ) -> str:
        tx: Dict = self._build_transaction(*args)
        return sender.transact(
            {
                "from": sender.address,
                "value": Wei(amount),
                "nonce": nonce if nonce is not None else sender.nonce,
                "gasPrice": Wei(gas_price) or tx["gasPrice"],
                "gas": Wei(gas_limit) or tx["gas"],
                "data": tx["data"],
            },
        )

    def _build_transaction(self, *args: Tuple) -> Dict:
        return self._instance.constructor(*args).buildTransaction()

    def estimate_gas(self, *args: Tuple) -> int:
        return self._instance.constructor(*args).estimateGas()
