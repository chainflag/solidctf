#!/usr/bin/env python3
from typing import Dict, List, Optional, Tuple

from web3 import Web3
from brownie.convert.utils import build_function_selector


class Contract:
    def __init__(self, web3: Web3, build: Dict) -> None:
        self._build = build.copy()
        self.bytecode = build["bytecode"]
        self.instance = web3.eth.contract(
            abi=self.abi,
            bytecode=self.bytecode
        )
        self.deploy = ContractConstructor(self)

        self.selectors = {
            build_function_selector(i): i["name"] for i in self.abi if i["type"] == "function"
        }

    @property
    def abi(self) -> List:
        return self._build["abi"]

    @property
    def name(self) -> str:
        return self._build["contractName"]

    def get_method(self, calldata: str) -> Optional[str]:
        sig = calldata[:10].lower()
        return self.selectors.get(sig)


class ContractConstructor:
    def __init__(self, parent: "Contract") -> None:
        self._parent = parent

    def build_transaction(self, *args: Tuple) -> Dict:
        return self._parent.instance.constructor(*args).buildTransaction()

    def estimate_gas(self, *args: Tuple) -> int:
        return self._parent.instance.constructor(*args).estimateGas()
