from typing import Any, Dict, Optional, Union

import rlp
from brownie.exceptions import VirtualMachineError
from eth_typing import ChecksumAddress, HexStr
from eth_utils import keccak, to_checksum_address
from hexbytes import HexBytes
from web3 import Web3
from web3.contract import ContractConstructor
from web3.exceptions import ContractLogicError, ValidationError
from web3.types import ABI


class Account:
    def __init__(self, private_key: Union[int, bytes, str] = None) -> None:
        if private_key is None:
            w3account = web3.eth.account.create()
        else:
            w3account = web3.eth.account.from_key(private_key)

        self._account = w3account
        self.address = self._account.address
        self.private_key = HexBytes(self._account.key).hex()

    def balance(self) -> int:
        balance = web3.eth.get_balance(self.address)
        return balance

    @property
    def nonce(self) -> int:
        return web3.eth.get_transaction_count(self.address)

    def get_deployment_address(self, nonce: Optional[int] = None) -> ChecksumAddress:
        if nonce is None:
            nonce = self.nonce

        address = HexBytes(self.address)
        raw = rlp.encode([address, nonce])
        deployment_address = HexBytes(keccak(raw)[12:]).hex()

        return to_checksum_address(deployment_address)

    def transact(self, tx: Dict) -> str:
        tx["chainId"] = web3.eth.chain_id
        tx["from"] = self.address
        tx["gasPrice"] = web3.eth.gas_price
        if "nonce" not in tx.keys():
            tx["nonce"] = self.nonce

        try:
            signed_tx = self._account.sign_transaction(tx).rawTransaction
            return web3.eth.send_raw_transaction(signed_tx).hex()
        except ValueError as e:
            raise VirtualMachineError(e) from None


class Contract:
    def __init__(self, abi: ABI, bytecode: HexStr) -> None:
        self.abi = abi
        self.bytecode = bytecode
        self.deploy = ContractCreation(self)

    def is_solved(
        self, address: ChecksumAddress, solved_event: str = None, tx_hash: HexStr = None
    ) -> bool:
        is_solved = False
        if solved_event:
            tx_receipt = web3.eth.get_transaction_receipt(tx_hash)
            block_interval: int = web3.eth.block_number - tx_receipt["blockNumber"]
            if block_interval > 128:
                raise ValidationError(
                    "cannot use transactions on blocks older than 128 blocks"
                )

            logs = (
                web3.eth.contract(abi=self.abi)
                .events[solved_event]()
                .processReceipt(tx_receipt)
            )
            for item in logs:
                if item["address"] == address:
                    is_solved = True
        else:
            try:
                is_solved = (
                    web3.eth.contract(address=address, abi=self.abi)
                    .functions.isSolved()
                    .call()
                )
            except ContractLogicError:
                return False

        return is_solved

    def constructor(self, args: Optional[Any] = None) -> ContractConstructor:
        return ContractConstructor(web3, self.abi, self.bytecode, *args)


class ContractCreation:
    def __init__(self, parent: "Contract") -> None:
        self._parent = parent

    def __call__(
        self,
        sender: Account,
        value: int = 0,
        args: Optional[Any] = None,
        gas_limit: Optional[int] = None,
    ) -> str:
        return sender.transact(
            {
                "value": value,
                "gas": gas_limit or self._estimate_gas(value, args),
                "data": self._parent.constructor(args).data_in_transaction,
            },
        )

    def _estimate_gas(self, value: int = 0, args: Optional[Any] = None) -> int:
        return self._parent.constructor(args).estimateGas({"value": value})

    def estimate_total_value(
        self,
        value: int = 0,
        args: Optional[Any] = None,
        gas_limit: Optional[int] = None,
    ) -> int:
        gas_limit: int = gas_limit or self._estimate_gas(value, args)
        return value + gas_limit * web3.eth.gas_price


web3 = Web3()
