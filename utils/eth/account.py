#!/usr/bin/env python3
import threading
import rlp

from typing import Dict, Optional, Union

from eth_typing import ChecksumAddress
from eth_utils import keccak, to_checksum_address
from hexbytes import HexBytes
from web3 import Web3
from brownie.exceptions import VirtualMachineError


class Account:
    def __init__(self, web3: Web3 = None, private_key: Union[int, bytes, str] = None) -> None:
        self._web3 = web3 or Web3(Web3.HTTPProvider("null"))
        if private_key is None:
            w3account = self._web3.eth.account.create()
        else:
            w3account = self._web3.eth.account.from_key(private_key)

        self._lock = threading.Lock()
        self._account = w3account
        self.address = self._account.address
        self.private_key = HexBytes(self._account.key).hex()

    def balance(self) -> int:
        balance = self._web3.eth.get_balance(self.address)
        return balance

    @property
    def nonce(self) -> int:
        return self._web3.eth.get_transaction_count(self.address)

    def get_deployment_address(self, nonce: Optional[int] = None) -> ChecksumAddress:
        if nonce is None:
            nonce = self.nonce

        address = HexBytes(self.address)
        raw = rlp.encode([address, nonce])
        deployment_address = HexBytes(keccak(raw)[12:]).hex()

        return to_checksum_address(deployment_address)

    def transact(self, tx: Dict) -> str:
        tx["from"] = self.address
        with self._lock:
            try:
                signed_tx = self._account.sign_transaction(tx).rawTransaction  # type: ignore
                txid = self._web3.eth.send_raw_transaction(signed_tx)
            except ValueError as e:
                exc = VirtualMachineError(e)
                if not hasattr(exc, "txid"):
                    raise exc from None

        return txid.hex()
