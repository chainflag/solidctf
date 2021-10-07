import json
import os

import pyseto

from dataclasses import dataclass
from glob import glob
from typing import Callable, List, Any

from eth_typing import HexStr
from eth_utils import to_checksum_address

from eth_challenge_base.config import Config
from eth_challenge_base.utils import Account, Contract


@dataclass
class Action:
    description: str
    handler: Callable[[], int]


class ActionHandler:
    def __init__(self, build_path: str, config: Config) -> None:
        with open(os.path.join(build_path, f"{config.contract}.json")) as fp:
            build_json = json.load(fp)
        self._contract: Contract = Contract(build_json)
        self._token_key = pyseto.Key.new(version=4, purpose="local", key=os.getenv("TOKEN_SECRET", ""))

        self._actions: List[Action] = [self._create_account_action(config.constructor_args),
                                       self._deploy_contract_action(config.constructor_value, config.constructor_args),
                                       self._get_flag_action(config.flag, config.solved_event)]
        if config.show_source:
            self._actions.append(self._show_source_action(build_path))

    def __getitem__(self, index: int) -> Action:
        return self._actions[index]

    def __len__(self):
        return len(self._actions)

    def _create_account_action(self, constructor_args: Any) -> Action:
        def action() -> int:
            account: Account = Account()
            print(f"[+]deployer account: {account.address}")
            token: str = pyseto.encode(self._token_key, payload=account.private_key).decode("utf-8")
            print(f"[+]token: {token}")
            estimate_gas: int = self._contract.deploy.estimate_gas(constructor_args)
            print(f"[+]it will cost {estimate_gas} gas to deploy, make sure that deployer account has enough ether!")
            return 0

        return Action(description="Create an account which will be used to deploy the challenge contract", handler=action)

    def _deploy_contract_action(self, constructor_value: int, constructor_args: Any) -> Action:
        def action() -> int:
            try:
                private_key: str = pyseto.decode(self._token_key, input("[-]input your token: ").strip()).payload.decode("utf-8")
            except ValueError as e:
                print(e)
                return 1

            account: Account = Account(private_key)
            if account.balance() == 0:
                print(f"[+]Don't forget to get some test ether for {account.address} first")
                return 1

            contract_addr: str = account.get_deployment_address()
            try:
                tx_hash: str = self._contract.deploy(account, constructor_value, constructor_args)
            except ValueError as e:
                print(e)
                return 1
            print(f"[+]contract address: {contract_addr}")
            print(f"[+]transaction hash: {tx_hash}")
            return 0

        return Action(description="Deploy the challenge contract using your generated account", handler=action)

    def _get_flag_action(self, flag: str, solved_event: str) -> Action:
        def action() -> int:
            try:
                private_key: str = pyseto.decode(self._token_key, input("[-]input your token: ").strip()).payload.decode("utf-8")
            except ValueError as e:
                print(e)
                return 1

            account: Account = Account(private_key)
            nonce: int = account.nonce
            if nonce == 0:
                print("[+]challenge contract has not yet been deployed")
                return 1

            contract_addr: str = account.get_deployment_address(nonce - 1)
            is_solved = False
            if solved_event:
                tx_hash = input(f"[-]input tx hash that emitted {solved_event} event: ").strip()
                logs = self._contract.get_events(solved_event, HexStr(tx_hash))
                for item in logs:
                    if item['address'] == contract_addr:
                        is_solved = True
            else:
                is_solved = self._contract.at(to_checksum_address(contract_addr)).isSolved().call()

            if is_solved:
                print(f"[+]flag: {flag}")
                return 0
            else:
                print("[+]it seems that you have not solved the challenge~~~~")
                return 1

        return Action(description="Get your flag once you meet the requirement", handler=action)

    def _show_source_action(self, build_path: str) -> Action:
        def action() -> int:
            for path in glob(os.path.join(build_path, "*.json")):
                try:
                    with open(path) as fp:
                        build_json = json.load(fp)
                except json.JSONDecodeError:
                    continue
                else:
                    print()
                    print(build_json["sourcePath"])
                    print(build_json["source"])

            return 0

        return Action(description="Show the contract source code", handler=action)
