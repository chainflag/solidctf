import yaml

from dataclasses import dataclass
from typing import Any


@dataclass(eq=False, frozen=True)
class Config:
    banner: str
    flag: str
    constructor_args: Any
    constructor_value: int


def parse_config(path: str) -> Config:
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    try:
        constructor_args = config["deploy"]["constructor_args"]
    except KeyError:
        constructor_args = None

    try:
        constructor_value = config["deploy"]["constructor_value"]
    except KeyError:
        constructor_value = 0

    return Config(config["banner"], config["flags"][0], constructor_args or tuple(), constructor_value)
