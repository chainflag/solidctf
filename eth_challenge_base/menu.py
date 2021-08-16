from eth_challenge_base.base import _MenuBase
from eth_challenge_base.config import Config
from eth_challenge_base.utils import Paseto, Build


class Menu(_MenuBase):
    def __init__(self, auth: Paseto, build: Build, config: Config) -> None:
        super().__init__(auth, build, config)
