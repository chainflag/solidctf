from dataclasses import dataclass
from typing import Callable, List

from eth_utils import to_checksum_address
from paseto import PasetoException

from eth_challenge_base.config import Config
from eth_challenge_base.utils import Paseto, Build, Account, Contract


@dataclass
class Action:
    name: str
    handler: Callable[[], int]


class ActionHandler:
    def __init__(self, auth: Paseto, build: Build, config: Config) -> None:
        self.auth: Paseto = auth
        self.build: Build = build
        self.config: Config = config
        self._actions: List[Action] = [Action(name="create deployer account", handler=self._create_deployer_account),
                                       Action(name="deploy challenge contract", handler=self._deploy_contract),
                                       Action(name="get flag", handler=self._get_flag)]
        self._contract: Contract = Contract(self.build.items()[0][1])

    def __getitem__(self, index: int) -> Action:
        return self._actions[index]

    def __len__(self):
        return len(self._actions)

    def _create_deployer_account(self) -> int:
        account: Account = Account()
        token: str = self.auth.create_token({"pk": account.private_key})
        print("[+]Your game account: {}".format(account.address))
        print("[+]token: {}".format(token))
        estimate_gas: int = self._contract.deploy.estimate_gas(*self.config.constructor_args)
        print("[+]Deploy will cost {} gas".format(estimate_gas))
        print("[+]Make sure that you have enough ether to deploy!!!!!!")
        return 0

    def _deploy_contract(self) -> int:
        try:
            message: dict = self.auth.parse_token(input("[-]input your token: ").strip())
        except PasetoException as e:
            print(f"Invalid token: {e}")
            return 1

        account: Account = Account(message["pk"])
        if account.balance() == 0:
            print("Insufficient balance of {}".format(account.address))
            return 1

        contract_addr: str = account.get_deployment_address()
        tx_hash: str = self._contract.deploy(account, self.config.constructor_value, *self.config.constructor_args)
        print("[+]Contract address: {}".format(contract_addr))
        print("[+]Transaction hash: {}".format(tx_hash))
        return 0

    def _get_flag(self) -> int:
        try:
            message: dict = self.auth.parse_token(input("[-]input your token: ").strip())
        except PasetoException as e:
            print(f"Invalid token: {e}")
            return 1

        account: Account = Account(message["pk"])
        contract_addr: str = account.get_deployment_address(account.nonce - 1)
        is_solved = self._contract.at(to_checksum_address(contract_addr)).isSolved().call()
        if is_solved:
            print("[+]flag: {}".format(self.config.flag))
            return 0
        else:
            print("[+]sorry, it seems that you have not solved this~~~~")
            return 1
