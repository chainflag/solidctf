#!/usr/bin/env python3
from typing import Dict, List, Optional, Tuple

from web3 import Web3
from brownie.convert import Wei
from brownie.convert.utils import build_function_selector

from helper.account import Account


class Contract:
    def __init__(self, web3: Web3, build: Dict) -> None:
        self.web3 = web3
        self._build = build.copy()
        self.bytecode = build["bytecode"]
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
        self.instance = parent.web3.eth.contract(
            abi=parent.abi,
            bytecode=parent.bytecode
        )

    def __call__(
            self,
            account: Account,
            *args: Tuple,
            amount: int = 0,
            gas_limit: Optional[int] = None,
            gas_price: Optional[int] = None,
            nonce: Optional[int] = None,
    ) -> str:
        tx: Dict = self._build_transaction(*args)
        return account.transact(  # type: ignore
            {
                "from": account.address,
                "value": Wei(amount),
                "nonce": nonce if nonce is not None else account.nonce,
                "gasPrice": Wei(gas_price) or tx["gasPrice"],
                "gas": Wei(gas_limit) or tx["gas"],
                "data": tx["data"],
            },
        )

    def _build_transaction(self, *args: Tuple) -> Dict:
        return self.instance.constructor(*args).buildTransaction()

    def estimate_gas(self, *args: Tuple) -> int:
        return self.instance.constructor(*args).estimateGas()
