"""Key derivation utilities (PBKDF2 placeholder)."""
import hashlib

def derive_key(password: str, salt: bytes, iterations: int = 100_000) -> bytes:
    """Derive a key using PBKDF2-HMAC-SHA256 (placeholder).
    This uses hashlib.pbkdf2_hmac for a simple default.
    """
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations)
