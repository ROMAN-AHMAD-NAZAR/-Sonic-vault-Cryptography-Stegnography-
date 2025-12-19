"""Basic encode example (placeholder)."""

from src.audio.binary_encoder import BinaryEncoder

if __name__ == '__main__':
    enc = BinaryEncoder()
    print(enc.encode(b"Hello"))
