import sys

from typing import List, Dict

from core.account import Account
from core.build import Build
from core.contract import Contract

menu: str = '''
We design a pretty easy contract game. Enjoy it!
1. Create a game account
2. Deploy a game contract
3. Request for flag
4. Get source code
Option 1, get an account which will be used to deploy the contract;
Before option 2, please transfer some eth to this account (for gas);
Option 2, the robot will use the account to deploy the contract for the problem;
Option 3, use this option to obtain the flag after the event is triggered.
Option 4, use this option to get source code.
You can finish this challenge in a lot of connections.
'''


class _MenuBase:
    def __init__(self) -> None:
        self._build: Build = Build("challenge")
        self._option: List = [None, self.create_game_account, self.deploy_contract, self.request_flag,
                              self.get_contract_source]

    def __str__(self) -> str:
        return menu

    def get_build_result(self, contract_name: str) -> Dict:
        return self._build.get(contract_name)

    def select_option(self, choice: int) -> None:
        if choice <= 0 or choice > 4:
            print("Invalid option")
            sys.exit(0)
        self._option[choice]()

    def create_game_account(self) -> None:
        pass

    def deploy_contract(self) -> None:
        pass

    def request_flag(self) -> None:
        pass

    def get_contract_source(self) -> None:
        pass


class Menu(_MenuBase):
    def __init__(self) -> None:
        super().__init__()
        self._contract: Contract = Contract(super().get_build_result("Greeter"))

    def create_game_account(self) -> None:
        account: Account = Account()
        print(account.address)
        print(account.private_key)
        estimate_gas: int = self._contract.deploy.estimate_gas("HelloWorld")
        print(estimate_gas)

    def deploy_contract(self) -> None:
        account: Account = Account()
        if account.balance() == 0:
            print("Insufficient balance")
            sys.exit(0)
        print(account.get_contract_address())
        tx_hash: str = account.deploy(self._contract, "HelloWorld")
        print(tx_hash)

    def request_flag(self) -> None:
        pass

    def get_contract_source(self) -> None:
        print(self._contract.source)
