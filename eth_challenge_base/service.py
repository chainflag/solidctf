import json
import os
import secrets
from decimal import Decimal
from glob import glob
from typing import Dict

import pyseto
from eth_typing import ChecksumAddress, HexStr
from eth_utils import units
from pyseto import Token
from twirp import ctxkeys, errors
from twirp.asgi import TwirpASGIApp
from twirp.exceptions import InvalidArgument, RequiredArgument, TwirpServerException

from eth_challenge_base.config import Config, parse_config
from eth_challenge_base.ethereum import Account, Contract
from eth_challenge_base.protobuf import challenge_pb2, challenge_twirp

AUTHORIZATION_KEY = "authorization"


class ChallengeService(object):
    def __init__(self, artifact_path: str, config: Config) -> None:
        self._config = config
        with open(os.path.join(artifact_path, f"{self._config.contract}.json")) as fp:
            build_json = json.load(fp)
        self._contract: Contract = Contract(build_json["abi"], build_json["bytecode"])
        self._source_code: Dict[str, str] = self._load_challenge_source(artifact_path)
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
        )

    def NewPlayground(self, context, empty):
        account: Account = Account()
        token: str = pyseto.encode(
            self._token_key, payload=account.private_key, footer=self._config.contract
        ).decode("utf-8")

        try:
            constructor = self._config.constructor
            total_value: int = self._contract.deploy.estimate_total_value(
                constructor.value, constructor.gas_limit, constructor.args
            )
        except Exception as e:
            raise TwirpServerException(
                code=errors.Errors.Internal,
                message=str(e),
            )

        ether_value: Decimal = Decimal(total_value) / units.units["ether"] + Decimal(
            "0.0005"
        )

        context.get_logger().info("Playground account %s was created", account.address)
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

        contract_addr: str = account.get_deployment_address()
        try:
            constructor = self._config.constructor
            tx_hash: str = self._contract.deploy(
                account, constructor.value, constructor.gas_limit, constructor.args
            )
        except Exception as e:
            raise TwirpServerException(
                code=errors.Errors.Internal,
                message=str(e),
            )

        context.get_logger().info(
            "Contract %s was deployed by %s. Transaction hash %s",
            contract_addr,
            account.address,
            tx_hash,
        )
        return challenge_pb2.Contract(address=contract_addr, tx_hash=tx_hash)

    def GetFlag(self, context, event):
        account: Account = self._recoverAcctFromCtx(context)
        nonce: int = account.nonce
        if nonce == 0:
            raise TwirpServerException(
                code=errors.Errors.FailedPrecondition,
                message="challenge contract has not yet been deployed",
            )
        contract_addr: ChecksumAddress = account.get_deployment_address(nonce - 1)

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

        context.get_logger().info(
            "Flag was captured in contract %s deployed by %s",
            contract_addr,
            account.address,
        )
        return challenge_pb2.Flag(flag=self._config.flag)

    def GetSourceCode(self, context, token):
        return challenge_pb2.SourceCode(source=self._source_code)

    def _load_challenge_source(self, artifact_path) -> Dict[str, str]:
        source: Dict[str, str] = {}
        if not self._config.show_source:
            return source
        for path in glob(os.path.join(artifact_path, "*.json")):
            try:
                with open(path) as fp:
                    build_json = json.load(fp)
            except json.JSONDecodeError:
                continue
            else:
                source_path: str = build_json["sourcePath"]
                source[source_path] = build_json["source"]

        return source

    def _recoverAcctFromCtx(self, context) -> Account:
        header = context.get(ctxkeys.RAW_HEADERS)
        token = header.get(AUTHORIZATION_KEY)
        if not token:
            raise RequiredArgument(argument="authorization")

        try:
            decoded_token: Token = pyseto.decode(self._token_key, token.strip())
        except Exception as e:
            raise TwirpServerException(
                code=errors.Errors.Unauthenticated, message=str(e)
            )

        if self._config.contract != decoded_token.footer.decode("utf-8"):
            raise TwirpServerException(
                code=errors.Errors.Unauthenticated,
                message="token was not issued by this challenge",
            )

        return Account(decoded_token.payload.decode("utf-8"))


def create_asgi_application(project_root: str) -> TwirpASGIApp:
    config = parse_config(os.path.join(project_root, "challenge.yml"))
    artifact_path = os.path.join(project_root, "build", "contracts")

    application = TwirpASGIApp()
    service = ChallengeService(artifact_path, config)
    application.add_service(challenge_twirp.ChallengeServer(service=service))
    return application
