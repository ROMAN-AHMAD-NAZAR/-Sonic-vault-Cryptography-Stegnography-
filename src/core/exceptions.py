"""Custom exceptions for sonic_vault."""

class SonicVaultError(Exception):
    pass

class CryptoError(SonicVaultError):
    pass

class AudioError(SonicVaultError):
    pass
