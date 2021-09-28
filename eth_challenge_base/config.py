import yaml

from dataclasses import dataclass
from typing import Any


@dataclass(eq=False, frozen=True)
class Config:
    description: str
    flag: str
    contract: str
    show_source: bool
    solved_event: str
    constructor_args: Any
    constructor_value: int


def parse_config(path: str) -> Config:
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    show_source = config.get("show_source", True)
    solved_event = config.get("solved_event", "")
    constructor = config.get("constructor", {})

    return Config(config["description"], config["flag"], config["contract"], show_source, solved_event,
                  constructor.get("args", ()), constructor.get("value", 0))
