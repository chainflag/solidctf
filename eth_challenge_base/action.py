import json
import os

from binascii import unhexlify
from dataclasses import dataclass
from typing import Callable, List

from eth_typing import HexStr
from eth_utils import to_checksum_address
from paseto import PasetoException

from eth_challenge_base.config import Config
from eth_challenge_base.utils import Paseto, Account, Contract


@dataclass
class Action:
    name: str
    handler: Callable[[], int]


class ActionHandler:
    def __init__(self, config: Config, project_path: str) -> None:
        exp_seconds = int(os.getenv("TOKEN_EXP_SECONDS")) if os.getenv("TOKEN_EXP_SECONDS") else None
        self._auth = Paseto(unhexlify(os.getenv("TOKEN_SECRET").encode("ascii")), exp_seconds=exp_seconds)
        self._actions: List[Action] = [self._create_account_action(), self._deploy_contract_action(config.payable_value),
                                       self._get_flag_action(config.flag, config.solved_event)]

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
            print(f"[+]deployer account: {account.address}")
            print(f"[+]token: {token}")
            print(f"[+]it will cost {self._contract.deploy.estimate_gas()} gas to deploy, make sure that the deployer "
                  "account has enough ether!")
            return 0

        return Action(name="create deployer account", handler=action)

    def _deploy_contract_action(self, payable_value: int) -> Action:
        def action() -> int:
            try:
                message: dict = self._auth.parse_token(input("[-]input your token: ").strip())
            except PasetoException as e:
                print(f"[+]invalid token: {e}")
                return 1

            account: Account = Account(message["pk"])
            if account.balance() == 0:
                print(f"[+]insufficient balance of {account.address}")
                return 1

            contract_addr: str = account.get_deployment_address()
            tx_hash: str = self._contract.deploy(account, payable_value)
            print(f"[+]setup contract:   {contract_addr}")
            print(f"[+]transaction hash: {tx_hash}")
            return 0

        return Action(name="deploy challenge contract", handler=action)

    def _get_flag_action(self, flag: str, solved_event: str) -> Action:
        def action() -> int:
            try:
                message: dict = self._auth.parse_token(input("[-]input your token: ").strip())
            except PasetoException as e:
                print(f"[+]invalid token: {e}")
                return 1

            account: Account = Account(message["pk"])
            nonce: int = account.nonce
            if nonce == 0:
                print("[+]challenge contract has not yet been deployed")
                return 1

            contract_addr: str = account.get_deployment_address(nonce - 1)
            is_solved = False
            if solved_event:
                tx_hash = input(f"[-]input tx hash that emitted {solved_event} event: ").strip()
                logs = self._contract.get_events(to_checksum_address(contract_addr), solved_event, HexStr(tx_hash))
                for item in logs:
                    if item['address'] == contract_addr:
                        is_solved = True
            else:
                is_solved = self._contract.at(to_checksum_address(contract_addr)).functions.isSolved().call()

            if is_solved:
                print(f"[+]flag: {flag}")
                return 0
            else:
                print("[+]it seems that you have not solved the challenge~~~~")
                return 1

        return Action(name="get flag", handler=action)
