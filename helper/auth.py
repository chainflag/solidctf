from paseto import create, parse


class Paseto:
    def __init__(self, key: bytes, purpose: str = "local", exp_seconds: int = None) -> None:
        self._key: bytes = key
        self._purpose: str = purpose
        self._exp_seconds: int = exp_seconds
        self._encoding: str = "utf-8"

    def create_token(self, claims: dict, exp_seconds: int = None) -> str:
        return create(
            key=self._key,
            purpose=self._purpose,
            claims=claims,
            exp_seconds=exp_seconds if exp_seconds is not None else self._exp_seconds
        ).decode(self._encoding)

    def parse_token(self, paseto_token: str) -> dict:
        parsed: dict = parse(
            key=self._key,
            purpose=self._purpose,
            token=paseto_token.encode(self._encoding),
        )
        return parsed['message']
