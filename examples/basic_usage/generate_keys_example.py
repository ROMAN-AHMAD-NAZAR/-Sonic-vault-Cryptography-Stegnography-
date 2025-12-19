"""Generate keys example (placeholder)."""
from src.crypto.dsa_manager import DSAKeyManager

if __name__ == '__main__':
    m = DSAKeyManager()
    print(m.generate_keypair())
