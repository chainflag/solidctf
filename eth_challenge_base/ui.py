import os
import sys
from dataclasses import dataclass
from typing import Callable, List

from twirp.context import Context
from twirp.exceptions import TwirpServerException

from eth_challenge_base.generated import challenge_pb2, challenge_twirp
from eth_challenge_base.service import AUTHORIZATION_KEY
from eth_challenge_base.utils import Powser


@dataclass
class Action:
    description: str
    handler: Callable[[], int]


class UserInterface:
    def __init__(self, address: str = "http://localhost:8000") -> None:
        self._client = challenge_twirp.ChallengeClient(address)
        self._info = self._client.GetChallengeInfo(
            ctx=Context(), request=challenge_pb2.Empty()
        )
        self._actions = self._create_actions()

    def __getitem__(self, index: int) -> Action:
        return self._actions[index]

    def __len__(self) -> int:
        return len(self._actions)

    def _create_actions(self) -> List[Action]:
        actions: List[Action] = []
        if not self._info.deployed_addr:
            actions = [
                Action(
                    "Create an account which will be used to deploy the challenge contract",
                    self._handle_new_playground,
                ),
                Action(
                    "Deploy the challenge contract using your generated account",
                    self._handle_deploy_contract,
                ),
            ]
        actions.append(
            Action("Get your flag once you meet the requirement", self._handle_get_flag)
        )
        if self._info.show_source:
            actions.append(
                Action("Show the contract source code", self._handle_get_sourcecode)
            )

        return actions

    def run(self) -> None:
        difficulty = int(os.getenv("POW_DIFFICULTY", "0"))
        if difficulty != 0:
            pow_challenge = Powser(difficulty)
            print(f"[+] {pow_challenge}")
            if not pow_challenge.verify_hash(input("[-] ??? = ")):
                print("[+] wrong proof")
                sys.exit(1)

        print(self._info.description)
        for i, action in enumerate(self._actions):
            print(f"[{i + 1}] - {action.description}")

        while True:
            choice = input("[-] input your choice: ")
            if not choice.isdigit():
                print("please enter a number.")
                continue
            choice = int(choice) - 1
            if 0 <= choice < len(self._actions):
                break
            print("invalid option, please try again.")

        sys.exit(self._actions[choice].handler())

    def _handle_new_playground(self) -> int:
        try:
            response = self._client.NewPlayground(
                ctx=Context(), request=challenge_pb2.Empty()
            )
        except TwirpServerException as e:
            print(e.message)
            return 1

        print(f"[+] deployer account: {response.address}")
        print(f"[+] token: {response.token}")
        print(
            f"[+] please transfer more than {round(response.value, 3)} test ether to the deployer account for next step"
        )

        return 0

    def _handle_deploy_contract(self) -> int:
        token: str = input("[-] input your token: ").strip()
        context = Context(headers={AUTHORIZATION_KEY: token})
        try:
            response = self._client.DeployContract(
                ctx=context, request=challenge_pb2.Empty()
            )
        except TwirpServerException as e:
            print(e.message)
            return 1

        print(f"[+] contract address: {response.address}")
        print(f"[+] transaction hash: {response.tx_hash}")
        return 0

    def _handle_get_flag(self) -> int:
        context = Context()
        if not self._info.deployed_addr:
            token: str = input("[-] input your token: ").strip()
            context.set_header(AUTHORIZATION_KEY, token)

        request = challenge_pb2.Event()
        if self._info.solved_event:
            tx_hash = input(
                f"[-] input tx hash that emitted {self._info.solved_event} event: "
            ).strip()
            request = challenge_pb2.Event(tx_hash=tx_hash)

        try:
            response = self._client.GetFlag(ctx=context, request=request)
        except TwirpServerException as e:
            print(e.message)
            return 1

        print(f"[+] flag: {response.flag}")
        return 0

    def _handle_get_sourcecode(self) -> int:
        try:
            response = self._client.GetSourceCode(
                ctx=Context(), request=challenge_pb2.Empty()
            )
        except TwirpServerException as e:
            print(e.message)
            return 1

        source = response.source
        for key, value in source.items():
            print(key)
            print(value)

        return 0
