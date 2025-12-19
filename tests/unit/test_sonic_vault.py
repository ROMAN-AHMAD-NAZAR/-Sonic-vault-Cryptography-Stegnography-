"""
Unit tests for SonicVault main application.
"""

import unittest
import sys
import os
import tempfile

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from core.sonic_vault import SonicVault

class TestSonicVault(unittest.TestCase):
    """Test cases for SonicVault class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.vault = SonicVault()
        self.test_message = "Test message for SonicVault"
        self.test_password = "TestPassword123!"
    
    def test_initialization(self):
        """Test SonicVault initialization."""
        self.assertIsNotNone(self.vault)
        self.assertIsNotNone(self.vault.aes)
        self.assertIsNotNone(self.vault.dsa)
        self.assertIsNotNone(self.vault.morse)
        self.assertIsNotNone(self.vault.encoder)
        self.assertIsNotNone(self.vault.sound_gen)
    
    def test_get_audio_themes(self):
        """Test getting audio themes."""
        themes = self.vault.get_audio_themes()
        self.assertIsInstance(themes, list)
        self.assertGreater(len(themes), 0)
        self.assertIn('sine', themes)
    
    def test_validate_password(self):
        """Test password validation."""
        # Test weak password
        is_valid, message = self.vault.validate_password("weak")
        self.assertFalse(is_valid)
        
        # Test strong password
        is_valid, message = self.vault.validate_password(self.test_password)
        self.assertTrue(is_valid)
    
    def test_get_system_info(self):
        """Test getting system information."""
        info = self.vault.get_system_info()
        self.assertIn('version', info)
        self.assertIn('components', info)
        self.assertIn('default_key_paths', info)
        self.assertEqual(info['version'], '1.0.0')
    
    def test_generate_keypair(self):
        """Test key pair generation."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='_private.pem') as private_file:
            private_path = private_file.name
        with tempfile.NamedTemporaryFile(delete=False, suffix='_public.pem') as public_file:
            public_path = public_file.name
        
        try:
            result = self.vault.generate_keypair(private_path, public_path)
            
            self.assertTrue(result['success'])
            self.assertEqual(result['private_key_path'], private_path)
            self.assertEqual(result['public_key_path'], public_path)
            self.assertTrue(os.path.exists(private_path))
            self.assertTrue(os.path.exists(public_path))
            
        finally:
            if os.path.exists(private_path):
                os.unlink(private_path)
            if os.path.exists(public_path):
                os.unlink(public_path)
    
    def test_encode_message_basic(self):
        """Test basic message encoding."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            output_path = temp_file.name
        
        try:
            result = self.vault.encode_message(
                message=self.test_message,
                password=self.test_password,
                output_file=output_path,
                theme='sine',
                sign=False  # Don't sign for basic test
            )
            
            self.assertTrue(result['success'])
            self.assertEqual(result['output_file'], output_path)
            self.assertEqual(result['theme'], 'sine')
            self.assertEqual(result['signed'], False)
            self.assertTrue(os.path.exists(output_path))
            self.assertGreater(os.path.getsize(output_path), 0)
            
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_encode_message_with_signature(self):
        """Test message encoding with digital signature."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as audio_file:
            audio_path = audio_file.name
        with tempfile.NamedTemporaryFile(delete=False, suffix='_private.pem') as private_file:
            private_path = private_file.name
        with tempfile.NamedTemporaryFile(delete=False, suffix='_public.pem') as public_file:
            public_path = public_file.name
        
        try:
            # First generate key pair
            self.vault.generate_keypair(private_path, public_path)
            
            # Encode with signature
            result = self.vault.encode_message(
                message=self.test_message,
                password=self.test_password,
                output_file=audio_path,
                theme='sine',
                sign=True,
                private_key_path=private_path
            )
            
            self.assertTrue(result['success'])
            self.assertEqual(result['signed'], True)
            self.assertTrue(os.path.exists(audio_path))
            
        finally:
            for path in [audio_path, private_path, public_path]:
                if os.path.exists(path):
                    os.unlink(path)
    
    def test_encode_message_invalid_theme(self):
        """Test encoding with invalid theme."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            output_path = temp_file.name
        
        try:
            with self.assertRaises(ValueError):
                self.vault.encode_message(
                    message=self.test_message,
                    password=self.test_password,
                    output_file=output_path,
                    theme='invalid_theme'
                )
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_encode_message_empty_inputs(self):
        """Test encoding with empty inputs."""
        with self.assertRaises(ValueError):
            self.vault.encode_message("", self.test_password, "test.wav")
        
        with self.assertRaises(ValueError):
            self.vault.encode_message(self.test_message, "", "test.wav")
        
        with self.assertRaises(ValueError):
            self.vault.encode_message(self.test_message, self.test_password, "")
    
    def test_encode_with_different_themes(self):
        """Test encoding with different audio themes."""
        themes = self.vault.get_audio_themes()
        
        for theme in themes:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                output_path = temp_file.name
            
            try:
                result = self.vault.encode_message(
                    message=self.test_message,
                    password=self.test_password,
                    output_file=output_path,
                    theme=theme,
                    sign=False
                )
                
                self.assertTrue(result['success'])
                self.assertEqual(result['theme'], theme)
                self.assertTrue(os.path.exists(output_path))
                
            finally:
                if os.path.exists(output_path):
                    os.unlink(output_path)


if __name__ == '__main__':
    unittest.main()
