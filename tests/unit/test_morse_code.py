"""
Unit tests for Morse code converter.
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from utils.morse_code import MorseCode

class TestMorseCode(unittest.TestCase):
    """Test cases for MorseCode class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.morse = MorseCode()
    
    def test_text_to_morse_basic(self):
        """Test basic text to Morse conversion."""
        self.assertEqual(self.morse.text_to_morse("SOS"), "... --- ...")
        self.assertEqual(self.morse.text_to_morse("HELLO"), ".... . .-.. .-.. ---")
    
    def test_morse_to_text_basic(self):
        """Test basic Morse to text conversion."""
        self.assertEqual(self.morse.morse_to_text("... --- ..."), "SOS")
        self.assertEqual(self.morse.morse_to_text(".... . .-.. .-.. ---"), "HELLO")
    
    def test_text_with_spaces(self):
        """Test conversion with spaces."""
        morse = self.morse.text_to_morse("HELLO WORLD")
        self.assertEqual(morse, ".... . .-.. .-.. --- / .-- --- .-. .-.. -..")
        
        text = self.morse.morse_to_text(".... . .-.. .-.. --- / .-- --- .-. .-.. -..")
        self.assertEqual(text, "HELLO WORLD")
    
    def test_numbers_and_punctuation(self):
        """Test conversion with numbers and punctuation."""
        self.assertEqual(self.morse.text_to_morse("123"), ".---- ..--- ...--")
        self.assertEqual(self.morse.text_to_morse("HELLO!"), ".... . .-.. .-.. --- -.-.--")
    
    def test_case_insensitivity(self):
        """Test that conversion is case insensitive."""
        lower_morse = self.morse.text_to_morse("hello")
        upper_morse = self.morse.text_to_morse("HELLO")
        self.assertEqual(lower_morse, upper_morse)
    
    def test_empty_string(self):
        """Test empty string handling."""
        self.assertEqual(self.morse.text_to_morse(""), "")
        self.assertEqual(self.morse.morse_to_text(""), "")
    
    def test_whitespace_handling(self):
        """Test whitespace normalization."""
        morse1 = self.morse.text_to_morse("  HELLO  ")
        morse2 = self.morse.text_to_morse("HELLO")
        self.assertEqual(morse1, morse2)
    
    def test_invalid_character(self):
        """Test handling of unsupported characters."""
        with self.assertRaises(ValueError):
            self.morse.text_to_morse("HELLO#")
    
    def test_invalid_morse_code(self):
        """Test handling of invalid Morse patterns."""
        with self.assertRaises(ValueError):
            self.morse.morse_to_text(".... . .-.. .-.. --- .-.-.-.-")  # Invalid pattern
    
    def test_round_trip(self):
        """Test round-trip conversion."""
        test_messages = [
            "SOS",
            "HELLO WORLD",
            "TEST 123!",
            "PYTHON PROGRAMMING",
            "MORSE CODE IS COOL"
        ]
        
        for message in test_messages:
            with self.subTest(message=message):
                morse = self.morse.text_to_morse(message)
                decoded = self.morse.morse_to_text(morse)
                self.assertEqual(message.upper(), decoded)
    
    def test_validate_text(self):
        """Test text validation."""
        self.assertTrue(self.morse.validate_text("HELLO"))
        self.assertTrue(self.morse.validate_text("HELLO WORLD 123!"))
        self.assertFalse(self.morse.validate_text("HELLO#"))
        self.assertFalse(self.morse.validate_text(""))
    
    def test_get_supported_characters(self):
        """Test getting supported characters."""
        chars = self.morse.get_supported_characters()
        self.assertIn('A', chars)
        self.assertIn('1', chars)
        self.assertIn('.', chars)
        self.assertIn(' ', chars)


if __name__ == '__main__':
    unittest.main()
