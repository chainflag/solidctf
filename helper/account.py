#!/usr/bin/env python3
import threading
import rlp

from typing import Dict, Optional, Union

from eth_typing import ChecksumAddress
from eth_utils import keccak, to_checksum_address
from hexbytes import HexBytes
from web3 import Web3
from brownie.convert import Wei
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

    def balance(self) -> Wei:
        balance = self._web3.eth.get_balance(self.address)
        return Wei(balance)

    @property
    def nonce(self) -> int:
        return self._web3.eth.get_transaction_count(self.address)

    def get_contract_address(self, tx_hash: Optional[str] = None, nonce: Optional[int] = None) -> ChecksumAddress:
        if tx_hash is not None:
            tx_receipt = self._web3.eth.get_transaction_receipt(tx_hash)
            return to_checksum_address(tx_receipt['contractAddress'])

        if nonce is None:
            nonce = self.nonce

        address = HexBytes(self.address)
        raw = rlp.encode([address, nonce])

        contract_addr = HexBytes(keccak(raw)[12:]).hex()
        return to_checksum_address(contract_addr)

    def transact(self, tx: Dict) -> str:
        tx["chainId"] = self._web3.eth.chain_id
        with self._lock:
            try:
                signed_tx = self._account.sign_transaction(tx).rawTransaction  # type: ignore
                txid = self._web3.eth.send_raw_transaction(signed_tx)
            except ValueError as e:
                exc = VirtualMachineError(e)
                if not hasattr(exc, "txid"):
                    raise exc from None

        return txid.hex()
