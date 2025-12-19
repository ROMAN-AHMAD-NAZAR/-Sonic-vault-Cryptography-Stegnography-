"""
Unit tests for AES manager.
"""

import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from crypto.aes_manager import AESManager

class TestAESManager(unittest.TestCase):
    """Test cases for AESManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.aes = AESManager()
        self.test_password = "TestPassword123!"
    
    def test_encrypt_decrypt_basic(self):
        """Test basic encryption and decryption."""
        plaintext = "Hello, SonicVault!"
        
        # Encrypt
        salt, iv, ciphertext = self.aes.encrypt(plaintext, self.test_password)
        
        # Verify components
        self.assertIsNotNone(salt)
        self.assertIsNotNone(iv)
        self.assertIsNotNone(ciphertext)
        self.assertGreater(len(ciphertext), 0)
        
        # Decrypt
        decrypted = self.aes.decrypt(salt, iv, ciphertext, self.test_password)
        self.assertEqual(plaintext, decrypted)
    
    def test_encrypt_decrypt_string_method(self):
        """Test encryption and decryption using string methods."""
        plaintext = "Secret message for testing"
        
        # Encrypt to string
        encrypted_string = self.aes.encrypt_to_string(plaintext, self.test_password)
        
        # Verify string format
        self.assertIsInstance(encrypted_string, str)
        self.assertGreater(len(encrypted_string), 0)
        
        # Decrypt from string
        decrypted = self.aes.decrypt_from_string(encrypted_string, self.test_password)
        self.assertEqual(plaintext, decrypted)
    
    def test_different_messages_produce_different_ciphertexts(self):
        """Test that same message produces different ciphertexts each time."""
        plaintext = "Same message"
        
        # Encrypt same message twice
        encrypted1 = self.aes.encrypt_to_string(plaintext, self.test_password)
        encrypted2 = self.aes.encrypt_to_string(plaintext, self.test_password)
        
        # Should be different due to random salt and IV
        self.assertNotEqual(encrypted1, encrypted2)
    
    def test_wrong_password_fails(self):
        """Test that wrong password causes decryption failure."""
        plaintext = "Secret message"
        encrypted_string = self.aes.encrypt_to_string(plaintext, self.test_password)
        
        # Try to decrypt with wrong password
        with self.assertRaises(ValueError):
            self.aes.decrypt_from_string(encrypted_string, "WrongPassword123!")
    
    def test_empty_message(self):
        """Test encryption and decryption of empty message."""
        plaintext = ""
        encrypted_string = self.aes.encrypt_to_string(plaintext, self.test_password)
        decrypted = self.aes.decrypt_from_string(encrypted_string, self.test_password)
        
        self.assertEqual(plaintext, decrypted)
    
    def test_special_characters(self):
        """Test encryption and decryption of special characters."""
        plaintext = "Message with special chars: !@#$%^&*()_+-=[]{}|;:,.<>?/`~"
        encrypted_string = self.aes.encrypt_to_string(plaintext, self.test_password)
        decrypted = self.aes.decrypt_from_string(encrypted_string, self.test_password)
        
        self.assertEqual(plaintext, decrypted)
    
    def test_long_message(self):
        """Test encryption and decryption of long message."""
        plaintext = "A" * 1000  # 1000 character message
        encrypted_string = self.aes.encrypt_to_string(plaintext, self.test_password)
        decrypted = self.aes.decrypt_from_string(encrypted_string, self.test_password)
        
        self.assertEqual(plaintext, decrypted)
    
    def test_password_validation(self):
        """Test password strength validation."""
        # Test weak passwords
        weak_passwords = [
            "short",
            "12345678",
            "abcdefgh",
            "ABCDEFGH"
        ]
        
        for password in weak_passwords:
            is_valid, message = self.aes.validate_password_strength(password)
            self.assertFalse(is_valid, f"Password '{password}' should be invalid")
        
        # Test strong passwords
        strong_passwords = [
            "StrongPass123!",
            "Another_Good1@",
            "My!Password123"
        ]
        
        for password in strong_passwords:
            is_valid, message = self.aes.validate_password_strength(password)
            self.assertTrue(is_valid, f"Password '{password}' should be valid")
    
    def test_corrupted_data_fails(self):
        """Test that corrupted encrypted data causes decryption failure."""
        plaintext = "Test message"
        encrypted_string = self.aes.encrypt_to_string(plaintext, self.test_password)
        
        # Corrupt the data by changing a character
        corrupted_string = encrypted_string[:-1] + ('A' if encrypted_string[-1] != 'A' else 'B')
        
        # Try to decrypt corrupted data
        with self.assertRaises(ValueError):
            self.aes.decrypt_from_string(corrupted_string, self.test_password)


if __name__ == '__main__':
    unittest.main()
