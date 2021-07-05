import yaml

from binascii import unhexlify
from dataclasses import dataclass
from typing import Any


@dataclass(eq=False, frozen=True)
class Config:
    flag: str
    banner: str
    secret: bytes
    exp_seconds: int
    web3_provider: str
    constructor_args: Any


def parse_config(path: str) -> Config:
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    _config = Config(flag=config["flag"], banner=config["banner"],
                     secret=unhexlify(config["auth_token"]["secret"].encode("ascii")),
                     exp_seconds=config["auth_token"]["exp_seconds"],
                     web3_provider=config["contract_deploy"]["web3_provider"],
                     constructor_args=config["contract_deploy"]["constructor_args"])
    return _config
