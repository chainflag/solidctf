#!/usr/bin/env python3
import eth_abi

from typing import Any, Dict, List, Optional, Union, Tuple
from hexbytes import HexBytes
from brownie.convert.normalize import format_input
from brownie.convert.utils import build_function_selector, build_function_signature, get_type_strings


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

    def decode_input(self, calldata: Union[str, bytes]) -> Tuple[str, Any]:
        if not isinstance(calldata, HexBytes):
            calldata = HexBytes(calldata)

        abi = next(
            (
                i
                for i in self.abi
                if i["type"] == "function" and build_function_selector(i) == calldata[:4].hex()
            ),
            None,
        )
        if abi is None:
            raise ValueError("Four byte selector does not match the ABI for this contract")

        function_sig = build_function_signature(abi)

        types_list = get_type_strings(abi["inputs"])
        result = eth_abi.decode_abi(types_list, calldata[4:])
        input_args = format_input(abi, result)

        return function_sig, input_args


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

    def encode_input(self, *args: tuple) -> str:
        bytecode = self._parent.bytecode
        data = format_input(self.abi, args)
        types_list = get_type_strings(self.abi["inputs"])
        return bytecode + eth_abi.encode_abi(types_list, data).hex()

    def estimate_gas(self) -> int:
        pass
