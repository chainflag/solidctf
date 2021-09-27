import yaml

from dataclasses import dataclass


@dataclass(eq=False, frozen=True)
class Config:
    description: str
    flag: str
    payable_value: int


def parse_config(path: str) -> Config:
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    try:
        payable_value = config["payable_value"]
    except KeyError:
        payable_value = 0

    return Config(config["description"], config["flag"], payable_value)
