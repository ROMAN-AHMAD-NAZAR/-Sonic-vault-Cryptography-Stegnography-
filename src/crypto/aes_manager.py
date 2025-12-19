"""
AES Encryption Manager for SonicVault
Handles AES-256 encryption and decryption of messages.
"""

import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from typing import Tuple
import secrets

class AESManager:
    """
    Handles AES-256 encryption and decryption using PBKDF2 for key derivation.
    """
    
    # Encryption configuration
    CONFIG = {
        'key_length': 32,      # 256 bits for AES-256
        'salt_length': 16,     # 128 bits for salt
        'iv_length': 16,       # 128 bits for IV
        'iterations': 100000,  # PBKDF2 iterations
    }
    
    def __init__(self):
        """Initialize the AES encryption manager."""
        self.backend = default_backend()
    
    def encrypt(self, plaintext: str, password: str) -> Tuple[bytes, bytes, bytes]:
        """
        Encrypt plaintext using AES-256-CBC with PBKDF2 key derivation.
        
        Args:
            plaintext (str): Text to encrypt
            password (str): Password for key derivation
            
        Returns:
            Tuple[bytes, bytes, bytes]: (salt, iv, ciphertext)
        """
        # Generate random salt and IV
        salt = secrets.token_bytes(self.CONFIG['salt_length'])
        iv = secrets.token_bytes(self.CONFIG['iv_length'])
        
        # Derive key from password
        key = self._derive_key(password, salt)
        
        # Pad the plaintext
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode('utf-8'))
        padded_data += padder.finalize()
        
        # Encrypt
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        return salt, iv, ciphertext
    
    def decrypt(self, salt: bytes, iv: bytes, ciphertext: bytes, password: str) -> str:
        """
        Decrypt ciphertext using AES-256-CBC.
        
        Args:
            salt (bytes): Salt used for key derivation
            iv (bytes): Initialization vector
            ciphertext (bytes): Encrypted data
            password (str): Password for key derivation
            
        Returns:
            str: Decrypted plaintext
            
        Raises:
            ValueError: If decryption fails (wrong password or corrupted data)
        """
        try:
            # Derive key from password
            key = self._derive_key(password, salt)
            
            # Decrypt
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
            decryptor = cipher.decryptor()
            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            
            # Unpad
            unpadder = padding.PKCS7(128).unpadder()
            plaintext = unpadder.update(padded_plaintext)
            plaintext += unpadder.finalize()
            
            return plaintext.decode('utf-8')
        
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}") from e
    
    def encrypt_to_string(self, plaintext: str, password: str) -> str:
        """
        Encrypt plaintext and return as a single base64 string.
        
        Args:
            plaintext (str): Text to encrypt
            password (str): Password for key derivation
            
        Returns:
            str: Base64 encoded string containing salt, iv, and ciphertext
        """
        salt, iv, ciphertext = self.encrypt(plaintext, password)
        
        # Combine all components
        combined = salt + iv + ciphertext
        
        # Encode as base64 for easy storage/transmission
        return base64.b64encode(combined).decode('utf-8')
    
    def decrypt_from_string(self, encrypted_data: str, password: str) -> str:
        """
        Decrypt from a single base64 string.
        
        Args:
            encrypted_data (str): Base64 string containing salt, iv, and ciphertext
            password (str): Password for key derivation
            
        Returns:
            str: Decrypted plaintext
        """
        # Decode base64
        combined = base64.b64decode(encrypted_data)
        
        # Extract components
        salt = combined[:self.CONFIG['salt_length']]
        iv = combined[self.CONFIG['salt_length']:self.CONFIG['salt_length'] + self.CONFIG['iv_length']]
        ciphertext = combined[self.CONFIG['salt_length'] + self.CONFIG['iv_length']:]
        
        return self.decrypt(salt, iv, ciphertext, password)
    
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """
        Derive encryption key from password using PBKDF2.
        
        Args:
            password (str): User password
            salt (bytes): Random salt
            
        Returns:
            bytes: Derived key
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.CONFIG['key_length'],
            salt=salt,
            iterations=self.CONFIG['iterations'],
            backend=self.backend
        )
        return kdf.derive(password.encode('utf-8'))
    
    def validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """
        Validate password strength.
        
        Args:
            password (str): Password to validate
            
        Returns:
            Tuple[bool, str]: (is_valid, message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if len(password) > 128:
            return False, "Password must be less than 128 characters"
        
        # Check for character variety
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        score = sum([has_upper, has_lower, has_digit, has_special])
        
        if score >= 3:
            return True, "Strong password"
        elif score >= 2:
            return True, "Moderate password"
        else:
            return False, "Password should include uppercase, lowercase, digits, and special characters"


# Example usage and testing
if __name__ == "__main__":
    aes = AESManager()
    
    # Test encryption and decryption
    test_messages = [
        "Hello, SonicVault!",
        "Secret meeting at midnight",
        "The quick brown fox jumps over the lazy dog",
        "1234567890!@#$%^&*()"
    ]
    
    test_password = "MyStrongPassword123!"
    
    print("AES Encryption Manager Test")
    print("=" * 50)
    
    # Test password strength
    is_valid, message = aes.validate_password_strength(test_password)
    print(f"Password validation: {message}")
    print()
    
    for i, message in enumerate(test_messages, 1):
        try:
            # Encrypt to string
            encrypted = aes.encrypt_to_string(message, test_password)
            
            # Decrypt from string
            decrypted = aes.decrypt_from_string(encrypted, test_password)
            
            print(f"Test {i}:")
            print(f"  Original:  '{message}'")
            print(f"  Encrypted: {encrypted[:50]}...")
            print(f"  Decrypted: '{decrypted}'")
            print(f"  Success:   {message == decrypted}")
            print()
            
        except Exception as e:
            print(f"Test {i} failed: {e}")
            print()
    
    # Test wrong password
    print("Testing wrong password:")
    try:
        encrypted = aes.encrypt_to_string("Secret message", test_password)
        wrong_decrypted = aes.decrypt_from_string(encrypted, "WrongPassword123!")
        print("ERROR: Decryption should have failed with wrong password!")
    except ValueError as e:
        print(f"✓ Correctly failed with wrong password: {e}")
