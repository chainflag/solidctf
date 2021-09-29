import yaml

from dataclasses import dataclass
from typing import Any


@dataclass(eq=False, frozen=True)
class Config:
    contract: str
    description: str
    flag: str
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
    constructor_args = constructor.get("args", ())
    constructor_value = constructor.get("value", 0)

    if constructor_value is None or constructor_value < 0:
        constructor_value = 0

    return Config(config["contract"], config["description"], config["flag"],
                  show_source, solved_event, constructor_args, constructor_value)
