import secrets
import hashlib

class PoWServer:
    def __init__(self, difficulty=5, prefix_length=8):
        self.difficulty = difficulty
        self.prefix = secrets.token_urlsafe(prefix_length)[:prefix_length].replace('-', 'b').replace('_', 'a')

    def verify_hash(self, answer) -> bool:
        h = hashlib.sha256()
        h.update((self.prefix + answer).encode())
        bits = ''.join(bin(i)[2:].zfill(8) for i in h.digest())
        return bits.endswith('0' * self.difficulty)
