"""Unit tests for DSA manager."""

import unittest
import sys
import os
import tempfile

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from crypto.dsa_manager import DSAManager

class TestDSAManager(unittest.TestCase):
    """Test cases for DSAManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.dsa = DSAManager()
        self.test_data = b"Test data for DSA signatures"
    
    def test_generate_keypair(self):
        """Test key pair generation."""
        private_key, public_key = self.dsa.generate_keypair()
        
        self.assertIsNotNone(private_key)
        self.assertIsNotNone(public_key)
    
    def test_sign_and_verify(self):
        """Test signing and verification."""
        private_key, public_key = self.dsa.generate_keypair()
        
        # Sign data
        signature = self.dsa.sign_data(self.test_data, private_key)
        self.assertIsNotNone(signature)
        self.assertGreater(len(signature), 0)
        
        # Verify signature
        is_valid = self.dsa.verify_signature(self.test_data, signature, public_key)
        self.assertTrue(is_valid)
    
    def test_verify_wrong_data(self):
        """Test verification with wrong data."""
        private_key, public_key = self.dsa.generate_keypair()
        signature = self.dsa.sign_data(self.test_data, private_key)
        
        # Verify with wrong data
        wrong_data = self.test_data + b"modified"
        is_valid = self.dsa.verify_signature(wrong_data, signature, public_key)
        self.assertFalse(is_valid)
    
    def test_verify_wrong_signature(self):
        """Test verification with wrong signature."""
        private_key, public_key = self.dsa.generate_keypair()
        signature = self.dsa.sign_data(self.test_data, private_key)
        
        # Modify signature
        wrong_signature = signature[:-1] + bytes([signature[-1] ^ 0xFF])
        is_valid = self.dsa.verify_signature(self.test_data, wrong_signature, public_key)
        self.assertFalse(is_valid)
    
    def test_key_serialization(self):
        """Test key serialization and deserialization."""
        private_key, public_key = self.dsa.generate_keypair()
        
        # Serialize keys
        private_bytes = self.dsa.private_key_to_bytes(private_key)
        public_bytes = self.dsa.public_key_to_bytes(public_key)
        
        self.assertIsNotNone(private_bytes)
        self.assertIsNotNone(public_bytes)
        self.assertGreater(len(private_bytes), 0)
        self.assertGreater(len(public_bytes), 0)
        
        # Deserialize keys
        private_key_loaded = self.dsa.private_key_from_bytes(private_bytes)
        public_key_loaded = self.dsa.public_key_from_bytes(public_bytes)
        
        # Test that loaded keys work
        signature = self.dsa.sign_data(self.test_data, private_key_loaded)
        is_valid = self.dsa.verify_signature(self.test_data, signature, public_key_loaded)
        self.assertTrue(is_valid)
    
    def test_key_serialization_with_password(self):
        """Test key serialization with password protection."""
        private_key, public_key = self.dsa.generate_keypair()
        password = "TestPassword123!"
        
        # Serialize with password
        private_bytes = self.dsa.private_key_to_bytes(private_key, password)
        
        # Should fail to load without password
        with self.assertRaises(Exception):
            self.dsa.private_key_from_bytes(private_bytes)
        
        # Should load with correct password
        private_key_loaded = self.dsa.private_key_from_bytes(private_bytes, password)
        self.assertIsNotNone(private_key_loaded)
        
        # Test that loaded key works
        signature = self.dsa.sign_data(self.test_data, private_key_loaded)
        is_valid = self.dsa.verify_signature(self.test_data, signature, public_key)
        self.assertTrue(is_valid)
    
    def test_save_and_load_keypair(self):
        """Test saving and loading key pair from files."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='_private.pem') as private_file:
            private_path = private_file.name
        with tempfile.NamedTemporaryFile(delete=False, suffix='_public.pem') as public_file:
            public_path = public_file.name
        
        try:
            # Generate and save keys
            private_key, public_key = self.dsa.generate_keypair()
            self.dsa.save_keypair(private_key, public_key, private_path, public_path)
            
            # Verify files exist
            self.assertTrue(os.path.exists(private_path))
            self.assertTrue(os.path.exists(public_path))
            self.assertGreater(os.path.getsize(private_path), 0)
            self.assertGreater(os.path.getsize(public_path), 0)
            
            # Load keys
            private_key_loaded, public_key_loaded = self.dsa.load_keypair(private_path, public_path)
            
            # Test loaded keys
            signature = self.dsa.sign_data(self.test_data, private_key_loaded)
            is_valid = self.dsa.verify_signature(self.test_data, signature, public_key_loaded)
            self.assertTrue(is_valid)
            
        finally:
            # Clean up
            if os.path.exists(private_path):
                os.unlink(private_path)
            if os.path.exists(public_path):
                os.unlink(public_path)
    
    def test_sign_and_combine(self):
        """Test combined signing and extraction."""
        private_key, public_key = self.dsa.generate_keypair()
        
        # Sign and combine
        combined = self.dsa.sign_and_combine(self.test_data, private_key)
        self.assertIsNotNone(combined)
        self.assertGreater(len(combined), len(self.test_data))
        
        # Verify and extract
        extracted_data, is_valid = self.dsa.verify_and_extract(combined, public_key)
        
        self.assertEqual(extracted_data, self.test_data)
        self.assertTrue(is_valid)
    
    def test_verify_and_extract_invalid(self):
        """Test extraction with invalid combined data."""
        private_key, public_key = self.dsa.generate_keypair()
        
        # Test with too short data
        short_data = b"short"
        extracted, is_valid = self.dsa.verify_and_extract(short_data, public_key)
        self.assertEqual(extracted, b'')
        self.assertFalse(is_valid)
        
        # Test with corrupted data
        combined = self.dsa.sign_and_combine(self.test_data, private_key)
        corrupted = combined[:-10]  # Remove last 10 bytes
        extracted, is_valid = self.dsa.verify_and_extract(corrupted, public_key)
        self.assertEqual(extracted, b'')
        self.assertFalse(is_valid)
    
    def test_different_keys_dont_work(self):
        """Test that keys from different pairs don't work together."""
        private_key1, public_key1 = self.dsa.generate_keypair()
        private_key2, public_key2 = self.dsa.generate_keypair()
        
        # Sign with key1
        signature = self.dsa.sign_data(self.test_data, private_key1)
        
        # Should not verify with key2
        is_valid = self.dsa.verify_signature(self.test_data, signature, public_key2)
        self.assertFalse(is_valid)


if __name__ == '__main__':
    unittest.main()

