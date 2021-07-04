#!/usr/bin/env python3
import threading
import rlp

from typing import Any, Dict, Optional, Tuple, Union

from eth_utils import keccak
from hexbytes import HexBytes
from web3 import Web3
from brownie.convert import EthAddress, Wei
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

    def get_contract_address(self, tx_hash: Optional[str] = None, nonce: Optional[int] = None) -> str:
        if tx_hash is not None:
            tx_receipt = self._web3.eth.get_transaction_receipt(tx_hash)
            return EthAddress(tx_receipt['contractAddress'])

        if nonce is None:
            nonce = self.nonce

        address = HexBytes(self.address)
        raw = rlp.encode([address, nonce])

        return EthAddress(keccak(raw)[12:])

    def deploy(
            self,
            contract: Any,
            *args: Tuple,
            amount: int = 0,
            gas_limit: Optional[int] = None,
            gas_price: Optional[int] = None,
            nonce: Optional[int] = None,
    ) -> str:
        construct_tx: Dict = contract.deploy.build_transaction(*args)
        with self._lock:
            try:
                tx_hash = self._transact(  # type: ignore
                    {
                        "from": self.address,
                        "value": Wei(amount),
                        "nonce": nonce if nonce is not None else self.nonce,
                        "gasPrice": gas_price if gas_price is not None else construct_tx["gasPrice"],
                        "gas": Wei(gas_limit) or construct_tx["gas"],
                        "data": construct_tx["data"],
                    },
                )
            except ValueError as e:
                exc = VirtualMachineError(e)
                if not hasattr(exc, "txid"):
                    raise exc from None

        return tx_hash

    def _transact(self, tx: Dict) -> str:
        tx["chainId"] = self._web3.eth.chain_id
        signed_tx = self._account.sign_transaction(tx).rawTransaction  # type: ignore
        return self._web3.eth.send_raw_transaction(signed_tx).hex()
