import sys

from typing import List

from eth_utils import to_checksum_address
from paseto import PasetoException

from eth_challenge_base.config import Config
from eth_challenge_base.utils import Paseto, Build, Account, Contract


class _MenuBase:
    def __init__(self, auth: Paseto, build: Build, config: Config) -> None:
        self.auth: Paseto = auth
        self.build: Build = build
        self.config: Config = config
        self._contract: Contract = Contract(self.build.items()[0][1])
        self._option: List = [None, self._create_game_account, self._deploy_contract, self._request_flag,
                              self._get_contract_source]

    def __str__(self) -> str:
        return self.config.banner

    def select_option(self, choice: int) -> None:
        if choice <= 0 or choice > 4:
            print("Invalid option")
            sys.exit(1)
        self._option[choice]()

    def private_key_from_token(self, token: str) -> str:
        try:
            message: dict = self.auth.parse_token(token.strip())
        except PasetoException as e:
            print(f"Invalid token: {e}")
            sys.exit(1)

        return message["pk"]

    def _create_game_account(self) -> None:
        account: Account = Account()
        token: str = self.auth.create_token({"pk": account.private_key})
        print("[+]Your game account: {}".format(account.address))
        print("[+]token: {}".format(token))
        estimate_gas: int = self._contract.deploy.estimate_gas(*self.config.constructor_args)
        print("[+]Deploy will cost {} gas".format(estimate_gas))
        print("[+]Make sure that you have enough ether to deploy!!!!!!")

    def _deploy_contract(self) -> None:
        token = input("[-]input your token: ")
        account: Account = Account(self.private_key_from_token(token))
        if account.balance() == 0:
            print("Insufficient balance of {}".format(account.address))
            sys.exit(1)

        contract_addr: str = account.get_deployment_address()
        tx_hash: str = self._contract.deploy(account, self.config.constructor_value, *self.config.constructor_args)
        print("[+]Contract address: {}".format(contract_addr))
        print("[+]Transaction hash: {}".format(tx_hash))

    def _request_flag(self) -> None:
        token = input("[-]input your token: ")
        account: Account = Account(self.private_key_from_token(token))
        contract_addr: str = account.get_deployment_address(account.nonce - 1)
        is_solved = self._contract.at(to_checksum_address(contract_addr)).isSolved().call()
        if is_solved:
            print("[+]flag: {}".format(self.config.flag))
        else:
            print("[+]sorry, it seems that you have not solved this~~~~")

    def _get_contract_source(self) -> None:
        for key, data in self.build.items():
            print(f"{key}.sol")
            print(data["source"])
