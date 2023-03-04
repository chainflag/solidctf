import json
import os
import secrets
from decimal import Decimal
from glob import glob

import pyseto
from eth_typing import ChecksumAddress, HexStr
from eth_utils import to_checksum_address, units
from twirp import ctxkeys, errors
from twirp.exceptions import InvalidArgument, RequiredArgument, TwirpServerException

from eth_challenge_base.config import Config
from eth_challenge_base.ethereum import Account, Contract
from eth_challenge_base.protobuf import challenge_pb2

AUTHORIZATION_KEY = "authorization"


class ChallengeService(object):
    def __init__(self, project_path: str, config: Config) -> None:
        self._config = config
        self._artifact_path = os.path.join(project_path, "build", "contracts")
        with open(os.path.join(self._artifact_path, f"{config.contract}.json")) as fp:
            build_json = json.load(fp)
        self._contract: Contract = Contract(build_json)
        self._token_key = pyseto.Key.new(
            version=4,
            purpose="local",
            key=os.getenv("TOKEN_SECRET", secrets.token_hex(32)),
        )

    def GetChallengeInfo(self, context, empty):
        return challenge_pb2.Info(
            description=self._config.description,
            show_source=self._config.show_source,
            solved_event=self._config.solved_event,
            deployed_addr=self._config.deployed_addr,
        )

    def NewPlayground(self, context, empty):
        account: Account = Account()
        token: str = pyseto.encode(self._token_key, payload=account.private_key).decode(
            "utf-8"
        )

        constructor = self._config.constructor
        total_value: int = self._contract.deploy.estimate_total_value(
            constructor.value, constructor.args, constructor.gas_limit
        )

        ether_value: Decimal = Decimal(total_value) / units.units["ether"] + Decimal(
            "0.0005"
        )

        return challenge_pb2.Playground(
            address=account.address,
            token=token,
            value=float(round(ether_value, 3)),
        )

    def DeployContract(self, context, empty):
        account: Account = self._recoverAcctFromCtx(context)
        if account.balance() == 0:
            raise TwirpServerException(
                code=errors.Errors.FailedPrecondition,
                message=f"send test ether to {account.address} first",
            )

        constructor = self._config.constructor
        try:
            tx_hash: str = self._contract.deploy(
                account, constructor.value, constructor.args, constructor.gas_limit
            )
        except Exception as e:
            raise TwirpServerException(
                code=errors.Errors.Internal,
                message=str(e),
            )

        contract_addr: str = account.get_deployment_address()
        return challenge_pb2.Contract(address=contract_addr, tx_hash=tx_hash)

    def GetFlag(self, context, event):
        if not self._config.deployed_addr:
            account: Account = self._recoverAcctFromCtx(context)
            nonce: int = account.nonce
            if nonce == 0:
                raise TwirpServerException(
                    code=errors.Errors.FailedPrecondition,
                    message="challenge contract has not yet been deployed",
                )
            contract_addr: ChecksumAddress = account.get_deployment_address(nonce - 1)
        else:
            contract_addr: ChecksumAddress = to_checksum_address(
                self._config.deployed_addr
            )

        if self._config.solved_event:
            if not event.HasField("tx_hash"):
                raise RequiredArgument(argument="tx_hash")
            tx_hash = event.tx_hash.strip()
            if not (
                len(tx_hash) == 66
                and tx_hash.startswith("0x")
                and all(c in "0123456789abcdef" for c in tx_hash[2:])
            ):
                raise InvalidArgument(argument="tx_hash", error="is invalid")

            try:
                is_solved = self._contract.is_solved(
                    contract_addr, self._config.solved_event, HexStr(tx_hash)
                )
            except Exception as e:
                raise TwirpServerException(
                    code=errors.Errors.FailedPrecondition,
                    message=str(e),
                )
        else:
            is_solved = self._contract.is_solved(contract_addr)

        if not is_solved:
            raise TwirpServerException(
                code=errors.Errors.InvalidArgument,
                message="you haven't solved this challenge",
            )
        return challenge_pb2.Flag(flag=self._config.flag)

    def GetSourceCode(self, context, token):
        if not self._config.show_source:
            return challenge_pb2.SourceCode()

        contract_source = dict()
        for path in glob(os.path.join(self._artifact_path, "*.json")):
            try:
                with open(path) as fp:
                    build_json = json.load(fp)
            except json.JSONDecodeError:
                continue
            else:
                source_path: str = build_json["sourcePath"]
                contract_source[source_path] = build_json["source"]

        return challenge_pb2.SourceCode(source=contract_source)

    def _recoverAcctFromCtx(self, context) -> Account:
        header = context.get(ctxkeys.RAW_HEADERS)
        token = header.get(AUTHORIZATION_KEY)
        if not token:
            raise RequiredArgument(argument="authorization")

        try:
            private_key: str = pyseto.decode(
                self._token_key, token.strip()
            ).payload.decode("utf-8")
        except Exception as e:
            raise TwirpServerException(
                code=errors.Errors.Unauthenticated, message=str(e)
            )

        return Account(private_key)
