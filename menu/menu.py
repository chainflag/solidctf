from config import Config
from menu.base import _MenuBase
from packages.utils import Build, Paseto


class Menu(_MenuBase):
    def __init__(self, auth: Paseto, build: Build, config: Config) -> None:
        super().__init__(auth, build, config)
