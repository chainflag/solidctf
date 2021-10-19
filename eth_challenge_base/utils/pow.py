import hashlib
import secrets


class Powser:
    def __init__(self, difficulty: int, prefix_length: int = 8):
        self._difficulty = difficulty
        self._prefix = (
            secrets.token_urlsafe(prefix_length)[:prefix_length]
            .replace("-", "b")
            .replace("_", "a")
        )

    def __str__(self):
        return f"sha256({ self._prefix } + ???).binary.endswith('{ '0' * self._difficulty }')"

    def verify_hash(self, answer: str) -> bool:
        h = hashlib.sha256()
        h.update((self._prefix + answer).encode())
        bits = "".join(bin(i)[2:].zfill(8) for i in h.digest())
        return bits.endswith("0" * self._difficulty)
