import hashlib
import hmac
import secrets


class PasswordHasher:
    """Versioned scrypt hashes with a random salt per password."""

    def hash(self, password: str) -> str:
        salt = secrets.token_bytes(16)
        digest = self._derive(password, salt)
        return f"scrypt$131072$8$1${salt.hex()}${digest.hex()}"

    def verify(self, password: str, encoded: str) -> bool:
        try:
            algorithm, n, r, p, salt_hex, digest_hex = encoded.split("$")
            # Only supported parameters are accepted, never arbitrary work factors from storage.
            if (algorithm, n, r, p) != ("scrypt", "131072", "8", "1"):
                return False
            salt, digest = bytes.fromhex(salt_hex), bytes.fromhex(digest_hex)
            if len(salt) != 16 or len(digest) != 64:
                return False
            return hmac.compare_digest(self._derive(password, salt), digest)
        except (ValueError, TypeError):
            return False

    @staticmethod
    def _derive(password: str, salt: bytes) -> bytes:
        return hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=2**17,
            r=8,
            p=1,
            maxmem=256 * 1024 * 1024,
            dklen=64,
        )
