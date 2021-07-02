#!/usr/bin/env python3
import eth_abi

from typing import Dict, List, Optional, Union, Tuple

from brownie.convert.normalize import format_input
from brownie.convert.utils import build_function_selector, get_type_strings

from helper.account import Account


class Contract:
    def __init__(self, build: Dict) -> None:
        self._build = build.copy()
        self.bytecode = build["bytecode"]
        self.deploy = ContractConstructor(self, self._name)
        self.selectors = {
            build_function_selector(i): i["name"] for i in self.abi if i["type"] == "function"
        }

    @property
    def abi(self) -> List:
        return self._build["abi"]

    @property
    def _name(self) -> str:
        return self._build["contractName"]

    def get_method(self, calldata: str) -> Optional[str]:
        sig = calldata[:10].lower()
        return self.selectors.get(sig)


class ContractConstructor:
    def __init__(self, parent: "Contract", name: str) -> None:
        self._parent = parent
        try:
            self.abi = next(i for i in parent.abi if i["type"] == "constructor")
            self.abi["name"] = "constructor"
        except Exception:
            self.abi = {"inputs": [], "name": "constructor", "type": "constructor"}
        self._name = name

    @property
    def payable(self) -> Union[list, str, bool]:
        if "payable" in self.abi:
            return self.abi["payable"]
        else:
            return self.abi["stateMutability"] == "payable"

    def encode_input(self, *args: Tuple) -> str:
        bytecode = self._parent.bytecode
        data = format_input(self.abi, args)
        types_list = get_type_strings(self.abi["inputs"])
        return bytecode + eth_abi.encode_abi(types_list, data).hex()

    def estimate_gas(self, *args: Tuple) -> int:
        return Account.estimate_gas(data=self.encode_input(*args))
