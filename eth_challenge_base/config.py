import yaml

from dataclasses import dataclass
from typing import Any


@dataclass(eq=False, frozen=True)
class Config:
    description: str
    flag: str
    contract: str
    solved_event: str
    constructor_args: Any
    constructor_value: int


def parse_config(path: str) -> Config:
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    contract = config.get("contract", "Setup")
    solved_event = config.get("solved_event", "")
    constructor = config.get("constructor", {})

    return Config(config["description"], config["flag"], contract, solved_event,
                  constructor.get("args", ()), constructor.get("value", 0))
