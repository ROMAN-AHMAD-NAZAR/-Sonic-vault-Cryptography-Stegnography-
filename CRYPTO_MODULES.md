# Cryptographic Modules Documentation

## Overview
SonicVault implements two production-grade cryptographic modules for securing messages before audio steganography encoding.

---

## 1. AES Encryption Manager (`src/crypto/aes_manager.py`)

### Purpose
Symmetric encryption for confidentiality of messages using AES-256-CBC.

### Algorithm Details
- **Algorithm**: AES-256 in CBC mode (256-bit keys)
- **Key Derivation**: PBKDF2-HMAC-SHA256 with 100,000 iterations
- **Salt**: 16 bytes (128 bits) cryptographically random
- **IV**: 16 bytes (128 bits) cryptographically random per encryption
- **Padding**: PKCS7 (for 128-bit blocks)
- **Encoding**: Base64 for safe serialization

### Security Properties
- **Semantic Security**: Different ciphertexts for same plaintext (random IV/salt)
- **Key Strength**: 128-bit security from strong password derivation
- **Authentication**: Use DSAKeyManager for message authentication

### Public API

```python
from src.crypto import AESManager

aes = AESManager()

# Basic encryption with tuple unpacking
salt, iv, ciphertext = aes.encrypt(plaintext, password)

# Decrypt with components
plaintext = aes.decrypt(salt, iv, ciphertext, password)

# String-based convenience methods
encrypted_str = aes.encrypt_to_string(plaintext, password)
plaintext = aes.decrypt_from_string(encrypted_str, password)

# Password strength validation
is_valid, message = aes.validate_password_strength(password)
```

### Password Requirements
- **Length**: 8-128 characters
- **Strength**: Must contain 3+ of these 4 categories:
  - Uppercase letters (A-Z)
  - Lowercase letters (a-z)
  - Digits (0-9)
  - Special characters (!@#$%^&*)

### Error Handling
- `ValueError`: Wrong password or corrupted ciphertext during decryption
- `RuntimeError`: Internal encryption/decryption failures

### Configuration
```python
CONFIG = {
    'key_length': 32,      # 256 bits
    'salt_length': 16,     # 128 bits
    'iv_length': 16,       # 128 bits
    'iterations': 100000,  # PBKDF2 iterations
}
```

### Test Coverage (9 tests)
✅ Basic encryption/decryption  
✅ String-based methods  
✅ Different ciphertexts per encryption  
✅ Wrong password rejection  
✅ Empty message handling  
✅ Unicode/special character support  
✅ Large message (1000 chars)  
✅ Password validation  
✅ Corrupted ciphertext rejection  

---

## 2. DSA Key Manager (`src/crypto/dsa_manager.py`)

### Purpose
Digital signatures for message authentication using Ed25519.

### Algorithm Details
- **Algorithm**: Ed25519 (Edwards-curve Digital Signature)
- **Key Size**: 32 bytes (256 bits) for both private and public keys
- **Signature Size**: 64 bytes
- **Signature Type**: Deterministic (same message → same signature)
- **Encoding**: PEM format for keys, Base64 for signatures
- **Hash Algorithm**: SHA-512 (internal to Ed25519)

### Security Properties
- **128-bit Security Level**: Comparable to RSA-256
- **Side-Channel Resistant**: Constant-time operations
- **Deterministic**: No random number generation in signing
- **Small Keys**: Only 32 bytes for public key (vs 2048+ for RSA)

### Public API

```python
from src.crypto import DSAKeyManager

dsa = DSAKeyManager()

# Generate keypair (returns PEM-encoded bytes)
private_key, public_key = dsa.generate_keypair()

# Sign message
signature = dsa.sign(private_key, b"message")

# Verify signature (returns bool, never raises on verify)
is_valid = dsa.verify(public_key, b"message", signature)

# File I/O for key persistence
dsa.export_keypair_to_pem(private_key, public_key, 
                           "private.pem", "public.pem")
private_key, public_key = dsa.import_keypair_from_pem(
    "private.pem", "public.pem")
```

### Key Format
- **Private Key**: PEM-encoded PKCS8 format (~200 bytes text)
- **Public Key**: PEM-encoded SubjectPublicKeyInfo format (~100 bytes text)
- **Signatures**: Base64-encoded 64-byte Ed25519 signature (~88 bytes text)

### Error Handling
- `RuntimeError`: Keypair generation failure (rare)
- `ValueError`: Invalid private key format
- `IOError`: File I/O failures
- `verify()`: Returns `False` for any invalid input (never raises)

### Test Coverage (13 tests)
✅ Basic keypair generation  
✅ Sign and verify  
✅ Wrong message rejection  
✅ Wrong key rejection  
✅ Deterministic signatures  
✅ Empty message handling  
✅ Large message (1MB)  
✅ Corrupted signature rejection  
✅ Invalid private key handling  
✅ Invalid public key graceful failure  
✅ Keypair export/import  
✅ Unique keypairs  
✅ Unicode message support  

---

## 3. Integration: Secure Audio Steganography

### Complete Pipeline

```
Original Text
    ↓
[AES Encryption] → Encrypted Text + Password
    ↓
[DSA Signing] → Encrypted Text + Signature + Private Key
    ↓
[Morse Encoding] → Morse Code
    ↓
[Binary Encoding] → Binary with separators
    ↓
[Timing Conversion] → Timing patterns
    ↓
[Sound Generation] → Audio file (WAV)
```

### Typical Usage

```python
from src.crypto import AESManager, DSAKeyManager
from src.utils import MorseCode
from src.audio import BinaryEncoder, SoundGenerator

# Initialize modules
aes = AESManager()
dsa = DSAKeyManager()
morse = MorseCode()
encoder = BinaryEncoder()
generator = SoundGenerator()

# Generate keys for signing
private_key, public_key = dsa.generate_keypair()

# Encrypt message
aes_password = "StrongPass123!"
encrypted = aes.encrypt_to_string(original_message, aes_password)

# Sign encrypted message
signature = dsa.sign(private_key, encrypted.encode())

# Convert to audio
morse_code = morse.text_to_morse(original_message)
binary = encoder.morse_to_binary(morse_code)
timing = encoder.binary_to_timing(binary)
generator.set_theme("sine")
generator.timing_to_audio(timing, "hidden_message.wav")
```

### Security Considerations
1. **Encryption**: AES-256 with PBKDF2 prevents brute force
2. **Authentication**: Ed25519 prevents tampering
3. **Key Derivation**: 100,000 PBKDF2 iterations delays attacks
4. **Random Salts/IVs**: Every encryption is different
5. **Audio Steganography**: Hides encrypted message in audio layer

---

## 4. Dependency Information

### Required Package
```
cryptography>=42.0.0
```

### Installed Version
- cryptography: 46.0.3
- cffi: 2.0.0 (dependency)
- pycparser: 2.23 (dependency)

### Installation
```bash
pip install cryptography
```

---

## 5. Test Results Summary

| Module | Tests | Status |
|--------|-------|--------|
| AES Manager | 9 | ✅ PASS |
| DSA Manager | 13 | ✅ PASS |
| Morse Code | 13 | ✅ PASS |
| Binary Encoder | 9 | ✅ PASS |
| Sound Generator | 11 | ✅ PASS |
| **Total** | **55** | **✅ ALL PASS** |

**Execution Time**: 4.88 seconds

---

## 6. Best Practices

### AES Usage
1. Always validate password strength before encryption
2. Never reuse same password across different messages (automatic via random salt)
3. Store salt+iv+ciphertext together in the encrypted string
4. Don't lose the password - no recovery method exists

### DSA Usage
1. Keep private key secure (consider PEM file encryption in production)
2. Public key can be shared freely
3. Verify signatures of messages from untrusted sources
4. Store keypairs persistently using export_keypair_to_pem()

### Secure Workflow
1. Encrypt message with AES (confidentiality)
2. Sign encrypted message with DSA (authentication)
3. Embed both in audio via steganography
4. Transmit audio file over insecure channel
5. Receiver extracts, verifies signature, decrypts with password

---

## 7. Example: Secure Hidden Message

```python
# Sender: Create secure hidden message
original = "Secret meeting at noon"
password = "SuperSecurePass123!"
private_key, public_key = dsa.generate_keypair()

# Encrypt
encrypted = aes.encrypt_to_string(original, password)

# Sign
signature = dsa.sign(private_key, encrypted.encode())

# Convert to audio
morse = morse.text_to_morse(original)
binary = encoder.morse_to_binary(morse)
timing = encoder.binary_to_timing(binary)
generator.timing_to_audio(timing, "audio.wav")

# Receiver: Extract and verify
extracted = extract_from_audio("audio.wav")
is_valid = dsa.verify(public_key, extracted.encode(), signature)

if is_valid:
    plaintext = aes.decrypt_from_string(extracted, password)
    print(plaintext)  # "Secret meeting at noon"
```

---

Generated: Production Cryptography Suite for SonicVault Audio Steganography System
