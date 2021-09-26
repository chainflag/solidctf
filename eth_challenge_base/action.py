import json
import os

from binascii import unhexlify
from dataclasses import dataclass
from typing import Callable, List

from eth_utils import to_checksum_address
from paseto import PasetoException

from eth_challenge_base.utils import Paseto, Account, Contract


@dataclass
class Action:
    name: str
    handler: Callable[[], int]


class ActionHandler:
    def __init__(self, flag: str, payable_value: int, project_path: str) -> None:
        exp_seconds = int(os.getenv("TOKEN_EXP_SECONDS")) if os.getenv("TOKEN_EXP_SECONDS") else None
        self._auth = Paseto(unhexlify(os.getenv("TOKEN_SECRET").encode("ascii")), exp_seconds=exp_seconds)
        self._actions: List[Action] = [self._create_account_action(), self._deploy_contract_action(payable_value),
                                       self._get_flag_action(flag)]

        with open(os.path.join(project_path, "build/contracts/Setup.json")) as fp:
            build_json = json.load(fp)
        self._contract: Contract = Contract(build_json)

    def __getitem__(self, index: int) -> Action:
        return self._actions[index]

    def __len__(self):
        return len(self._actions)

    def _create_account_action(self) -> Action:
        def action() -> int:
            account: Account = Account()
            token: str = self._auth.create_token({"pk": account.private_key})
            print("[+]Deployer account: {}".format(account.address))
            print("[+]token: {}".format(token))
            estimate_gas: int = self._contract.deploy.estimate_gas()
            print("[+]Deploy will cost {} gas".format(estimate_gas))
            print("[+]Make sure that you have enough ether to deploy!!!!!!")
            return 0

        return Action(name="create deployer account", handler=action)

    def _deploy_contract_action(self, payable_value: int) -> Action:
        def action() -> int:
            try:
                message: dict = self._auth.parse_token(input("[-]input your token: ").strip())
            except PasetoException as e:
                print(f"Invalid token: {e}")
                return 1

            account: Account = Account(message["pk"])
            if account.balance() == 0:
                print("Insufficient balance of {}".format(account.address))
                return 1

            contract_addr: str = account.get_deployment_address()
            tx_hash: str = self._contract.deploy(account, payable_value)
            print("[+]Setup contract:   {}".format(contract_addr))
            print("[+]Transaction hash: {}".format(tx_hash))
            return 0

        return Action(name="deploy challenge contract", handler=action)

    def _get_flag_action(self, flag: str) -> Action:
        def action() -> int:
            try:
                message: dict = self._auth.parse_token(input("[-]input your token: ").strip())
            except PasetoException as e:
                print(f"Invalid token: {e}")
                return 1

            account: Account = Account(message["pk"])
            contract_addr: str = account.get_deployment_address(account.nonce - 1)
            is_solved = self._contract.at(to_checksum_address(contract_addr)).isSolved().call()
            if is_solved:
                print("[+]flag: {}".format(flag))
                return 0
            else:
                print("[+]sorry, it seems that you have not solved the challenge~~~~")
                return 1

        return Action(name="get flag", handler=action)
