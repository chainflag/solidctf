from helper.auth import Paseto
from helper.build import Build
from menu.base import _MenuBase


class Menu(_MenuBase):
    def __init__(self, auth: Paseto, build: Build) -> None:
        super().__init__(auth, build)
