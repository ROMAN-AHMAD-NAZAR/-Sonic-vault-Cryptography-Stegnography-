"""
DSA Signature Manager for SonicVault
Handles DSA key generation, signing, and verification.
"""

import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
from typing import Tuple
import secrets


class DSAManager:
    """
    Handles DSA key generation, signing, and verification.
    """
    
    # DSA configuration
    CONFIG = {
        'key_size': 2048,      # 2048-bit DSA keys
        'hash_algorithm': hashes.SHA256(),
    }
    
    def __init__(self):
        """Initialize the DSA signature manager."""
        self.backend = default_backend()
    
    def generate_keypair(self) -> Tuple[dsa.DSAPrivateKey, dsa.DSAPublicKey]:
        """
        Generate a new DSA key pair.
        
        Returns:
            Tuple[dsa.DSAPrivateKey, dsa.DSAPublicKey]: Private and public keys
        """
        private_key = dsa.generate_private_key(
            key_size=self.CONFIG['key_size'],
            backend=self.backend
        )
        public_key = private_key.public_key()
        
        return private_key, public_key
    
    def sign_data(self, data: bytes, private_key: dsa.DSAPrivateKey) -> bytes:
        """
        Sign data using DSA private key.
        
        Args:
            data (bytes): Data to sign
            private_key (dsa.DSAPrivateKey): Private key for signing
            
        Returns:
            bytes: Digital signature
        """
        signature = private_key.sign(
            data,
            self.CONFIG['hash_algorithm']
        )
        return signature
    
    def verify_signature(self, data: bytes, signature: bytes, public_key: dsa.DSAPublicKey) -> bool:
        """
        Verify DSA signature.
        
        Args:
            data (bytes): Original data
            signature (bytes): Signature to verify
            public_key (dsa.DSAPublicKey): Public key for verification
            
        Returns:
            bool: True if signature is valid, False otherwise
        """
        try:
            public_key.verify(
                signature,
                data,
                self.CONFIG['hash_algorithm']
            )
            return True
        except InvalidSignature:
            return False
    
    def private_key_to_bytes(self, private_key: dsa.DSAPrivateKey, password: str = None) -> bytes:
        """
        Serialize private key to bytes.
        
        Args:
            private_key (dsa.DSAPrivateKey): Private key to serialize
            password (str, optional): Password for encryption
            
        Returns:
            bytes: Serialized private key
        """
        if password:
            encryption = serialization.BestAvailableEncryption(password.encode('utf-8'))
        else:
            encryption = serialization.NoEncryption()
        
        return private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption
        )
    
    def public_key_to_bytes(self, public_key: dsa.DSAPublicKey) -> bytes:
        """
        Serialize public key to bytes.
        
        Args:
            public_key (dsa.DSAPublicKey): Public key to serialize
            
        Returns:
            bytes: Serialized public key
        """
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    
    def private_key_from_bytes(self, key_data: bytes, password: str = None) -> dsa.DSAPrivateKey:
        """
        Load private key from bytes.
        
        Args:
            key_data (bytes): Serialized private key
            password (str, optional): Password for decryption
            
        Returns:
            dsa.DSAPrivateKey: Loaded private key
        """
        if password:
            password_bytes = password.encode('utf-8')
        else:
            password_bytes = None
        
        return serialization.load_pem_private_key(
            key_data,
            password=password_bytes,
            backend=self.backend
        )
    
    def public_key_from_bytes(self, key_data: bytes) -> dsa.DSAPublicKey:
        """
        Load public key from bytes.
        
        Args:
            key_data (bytes): Serialized public key
            
        Returns:
            dsa.DSAPublicKey: Loaded public key
        """
        return serialization.load_pem_public_key(
            key_data,
            backend=self.backend
        )
    
    def save_keypair(self, private_key: dsa.DSAPrivateKey, public_key: dsa.DSAPublicKey, 
                    private_path: str, public_path: str, password: str = None):
        """
        Save key pair to files.
        
        Args:
            private_key (dsa.DSAPrivateKey): Private key to save
            public_key (dsa.DSAPublicKey): Public key to save
            private_path (str): Path for private key file
            public_path (str): Path for public key file
            password (str, optional): Password for private key encryption
        """
        # Save private key
        private_bytes = self.private_key_to_bytes(private_key, password)
        with open(private_path, 'wb') as f:
            f.write(private_bytes)
        
        # Save public key
        public_bytes = self.public_key_to_bytes(public_key)
        with open(public_path, 'wb') as f:
            f.write(public_bytes)
    
    def load_keypair(self, private_path: str, public_path: str, password: str = None) -> Tuple[dsa.DSAPrivateKey, dsa.DSAPublicKey]:
        """
        Load key pair from files.
        
        Args:
            private_path (str): Path to private key file
            public_path (str): Path to public key file
            password (str, optional): Password for private key decryption
            
        Returns:
            Tuple[dsa.DSAPrivateKey, dsa.DSAPublicKey]: Loaded key pair
        """
        # Load private key
        with open(private_path, 'rb') as f:
            private_key = self.private_key_from_bytes(f.read(), password)
        
        # Load public key
        with open(public_path, 'rb') as f:
            public_key = self.public_key_from_bytes(f.read())
        
        return private_key, public_key
    
    def sign_and_combine(self, data: bytes, private_key: dsa.DSAPrivateKey) -> bytes:
        """
        Sign data and combine with original data.
        
        Args:
            data (bytes): Data to sign
            private_key (dsa.DSAPrivateKey): Private key for signing
            
        Returns:
            bytes: Combined data + signature
        """
        signature = self.sign_data(data, private_key)

        # Combine: data + signature + signature length (4 bytes)
        # (Length placed at end so verify can read it from the final 4 bytes)
        signature_length = len(signature).to_bytes(4, byteorder='big')
        combined = data + signature + signature_length
        
        return combined
    
    def verify_and_extract(self, combined_data: bytes, public_key: dsa.DSAPublicKey) -> Tuple[bytes, bool]:
        """
        Extract data and verify signature from combined data.
        
        Args:
            combined_data (bytes): Combined data + signature
            public_key (dsa.DSAPublicKey): Public key for verification
            
        Returns:
            Tuple[bytes, bool]: (original_data, verification_result)
        """
        try:
            # Extract signature length
            if len(combined_data) < 4:
                return b'', False
            
            signature_length = int.from_bytes(combined_data[-4:], byteorder='big')
            
            # Check if we have enough data
            if len(combined_data) < 4 + signature_length:
                return b'', False
            
            # Extract data and signature
            data = combined_data[:-4 - signature_length]
            signature = combined_data[-4 - signature_length:-4]
            
            # Verify signature
            is_valid = self.verify_signature(data, signature, public_key)
            
            return data, is_valid
            
        except Exception:
            return b'', False


# Example usage and testing
if __name__ == "__main__":
    dsa_mgr = DSAManager()
    
    print("DSA Signature Manager Test")
    print("=" * 50)
    
    # Generate key pair
    print("1. Generating DSA key pair...")
    private_key, public_key = dsa_mgr.generate_keypair()
    print("   ✓ Key pair generated successfully")
    
    # Test data
    test_data = b"Hello, SonicVault! This is a test message for DSA signatures."
    
    # Sign data
    print("2. Signing test data...")
    signature = dsa_mgr.sign_data(test_data, private_key)
    print(f"   ✓ Signature created: {len(signature)} bytes")
    
    # Verify signature
    print("3. Verifying signature...")
    is_valid = dsa_mgr.verify_signature(test_data, signature, public_key)
    print(f"   ✓ Signature valid: {is_valid}")
    
    # Test with wrong data
    print("4. Testing with modified data...")
    wrong_data = test_data + b"modified"
    is_valid_wrong = dsa_mgr.verify_signature(wrong_data, signature, public_key)
    print(f"   ✓ Wrong data rejected: {not is_valid_wrong}")
    
    # Test key serialization
    print("5. Testing key serialization...")
    private_bytes = dsa_mgr.private_key_to_bytes(private_key)
    public_bytes = dsa_mgr.public_key_to_bytes(public_key)
    print(f"   ✓ Private key serialized: {len(private_bytes)} bytes")
    print(f"   ✓ Public key serialized: {len(public_bytes)} bytes")
    
    # Test key deserialization
    print("6. Testing key deserialization...")
    private_key_loaded = dsa_mgr.private_key_from_bytes(private_bytes)
    public_key_loaded = dsa_mgr.public_key_from_bytes(public_bytes)
    
    # Verify loaded keys work
    signature2 = dsa_mgr.sign_data(test_data, private_key_loaded)
    is_valid2 = dsa_mgr.verify_signature(test_data, signature2, public_key_loaded)
    print(f"   ✓ Loaded keys work: {is_valid2}")
    
    # Test combined sign/verify
    print("7. Testing combined sign/verify...")
    combined = dsa_mgr.sign_and_combine(test_data, private_key)
    extracted_data, is_valid_combined = dsa_mgr.verify_and_extract(combined, public_key)
    
    print(f"   ✓ Combined data length: {len(combined)} bytes")
    print(f"   ✓ Data extracted correctly: {extracted_data == test_data}")
    print(f"   ✓ Combined signature valid: {is_valid_combined}")
    
    print("\nAll tests completed successfully! ✓")
