import sys

from typing import List

from web3 import Web3

from config import Config
from packages.eth import Account, Contract
from packages.utils import Build, Paseto


class _MenuBase:
    def __init__(self, auth: Paseto, build: Build, config: Config) -> None:
        self.auth: Paseto = auth
        self.build: Build = build
        self.config: Config = config
        self.web3: Web3 = Web3(Web3.HTTPProvider(self.config.web3_provider))
        self._contract: Contract = Contract(self.web3, self.build.items()[0][1])
        self._option: List = [None, self._create_game_account, self._deploy_contract, self._request_flag,
                              self._get_contract_source]

    def __str__(self) -> str:
        return self.config.banner

    def select_option(self, choice: int) -> None:
        if choice <= 0 or choice > 4:
            print("Invalid option")
            sys.exit(0)
        self._option[choice]()

    def _create_game_account(self) -> None:
        account: Account = Account()
        token: str = self.auth.create_token({"private_key": account.private_key})
        print("[+]Your game account: {}".format(account.address))
        print("[+]token: {}".format(token))
        estimate_gas: int = self._contract.deploy.estimate_gas(*self.config.constructor_args)
        print("[+]Deploy will cost {} gas".format(estimate_gas))
        print("[+]Make sure that you have enough ether to deploy!!!!!!")

    def _deploy_contract(self) -> None:
        token = input("[-]input your token: ")
        message: dict = self.auth.parse_token(token.strip())
        account: Account = Account(self.web3, message["private_key"])
        if account.balance() == 0:
            print("Insufficient balance of {}".format(account.address))
            sys.exit(0)

        contract_addr: str = account.get_contract_address()
        tx_hash: str = self._contract.deploy(*self.config.constructor_args, sender=account)
        print("[+]Contract address: {}".format(contract_addr))
        print("[+]Transaction hash: {}".format(tx_hash))
        print("[+]deployed token: {}".format(self.auth.create_token({"contract_addr": contract_addr})))

    def _request_flag(self) -> None:
        deployed_token = input("[-]input your deployed token: ")
        message: dict = self.auth.parse_token(deployed_token.strip())
        res = self._contract.at(message["contract_addr"]).isSolved().call()
        if res:
            print("[+]flag: {}".format(self.config.flag))
        else:
            print("[+]sorry, it seems that you have not solved this~~~~")

    def _get_contract_source(self) -> None:
        for key, data in self.build.items():
            print(f"{key}.sol")
            print(data["source"])
