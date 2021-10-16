from dataclasses import dataclass
from typing import Any

import yaml


@dataclass(eq=False, frozen=True)
class Constructor:
    args: Any
    value: int
    gas_limit: int


@dataclass(eq=False, frozen=True)
class Config:
    contract: str
    description: str
    flag: str
    show_source: bool
    solved_event: str
    deployed_addr: str
    constructor: Constructor


def parse_config(path: str) -> Config:
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    show_source = config.get("show_source", True)
    solved_event = config.get("solved_event", "")
    deployed_addr = config.get("deployed_addr", "")
    constructor = config.get("constructor", {})
    constructor_args = constructor.get("args", ())
    constructor_value = constructor.get("value", 0)
    constructor_gas = constructor.get("gas", 0)

    if constructor_value is None or constructor_value < 0:
        constructor_value = 0

    return Config(
        config["contract"],
        config["description"],
        config["flag"],
        show_source,
        solved_event,
        deployed_addr,
        Constructor(constructor_args, constructor_value, constructor_gas),
    )
