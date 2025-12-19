"""
Unit tests for binary encoder.
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from audio.binary_encoder import BinaryEncoder
from utils.morse_code import MorseCode

class TestBinaryEncoder(unittest.TestCase):
    """Test cases for BinaryEncoder class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.encoder = BinaryEncoder()
        self.morse = MorseCode()
    
    def test_morse_to_binary_basic(self):
        """Test basic Morse to binary conversion."""
        binary = self.encoder.morse_to_binary("... --- ...")
        expected = "000/111/000"  # SOS format
        self.assertEqual(binary, expected)
    
    def test_binary_to_morse_basic(self):
        """Test basic binary to Morse conversion."""
        binary_data = "000/111/000"
        morse = self.encoder.binary_to_morse(binary_data)
        self.assertEqual(morse, "... --- ...")
    
    def test_morse_to_binary_with_spaces(self):
        """Test Morse to binary with word spaces."""
        morse_code = ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
        binary = self.encoder.morse_to_binary(morse_code)
        # Should contain character separators
        self.assertIn('/', binary)
    
    def test_binary_to_timing_basic(self):
        """Test binary to timing pattern conversion."""
        binary_data = "0 1"  # dot then dash
        timings = self.encoder.binary_to_timing(binary_data)
        
        # Should have 2 timing patterns
        self.assertEqual(len(timings), 2)
        
        # First should be dot (short duration)
        dot_duration, dot_gap = timings[0]
        self.assertAlmostEqual(dot_duration, 0.2, places=2)  # 200ms
        
        # Second should be dash (long duration)  
        dash_duration, dash_gap = timings[1]
        self.assertAlmostEqual(dash_duration, 0.6, places=2)  # 600ms
    
    def test_timing_to_binary_basic(self):
        """Test timing pattern to binary conversion."""
        # Create test timings for dot and dash
        test_timings = [
            (0.2, 0.2),  # dot
            (0.6, 0.2),  # dash
        ]
        
        binary = self.encoder.timing_to_binary(test_timings)
        self.assertEqual(binary, "01")
    
    def test_round_trip_morse_binary(self):
        """Test round-trip Morse to binary and back."""
        test_morse_codes = [
            "... --- ...",
            ".... . .-.. .-.. ---",
            ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
        ]
        
        for morse_code in test_morse_codes:
            with self.subTest(morse_code=morse_code):
                binary = self.encoder.morse_to_binary(morse_code)
                morse_back = self.encoder.binary_to_morse(binary)
                self.assertEqual(morse_code, morse_back)
    
    def test_round_trip_binary_timing(self):
        """Test round-trip binary to timing and back."""
        test_binary_data = [
            "000",
            "0101",
            "000111000"
        ]
        
        for binary_data in test_binary_data:
            with self.subTest(binary_data=binary_data):
                timings = self.encoder.binary_to_timing(binary_data)
                binary_back = self.encoder.timing_to_binary(timings)
                self.assertEqual(binary_data, binary_back)
    
    def test_full_round_trip(self):
        """Test full round-trip: text -> Morse -> binary -> timing -> binary -> Morse -> text."""
        test_messages = ["SOS", "HELLO", "TEST"]
        
        for message in test_messages:
            with self.subTest(message=message):
                morse_code = self.morse.text_to_morse(message)
                binary_data = self.encoder.morse_to_binary(morse_code)
                timings = self.encoder.binary_to_timing(binary_data)
                binary_back = self.encoder.timing_to_binary(timings)
                morse_back = self.encoder.binary_to_morse(binary_back)
                text_back = self.morse.morse_to_text(morse_back)
                
                self.assertEqual(message.upper(), text_back)
    
    def test_custom_timing_config(self):
        """Test with custom timing configuration."""
        custom_config = {
            'dot_duration': 100,   # 100ms dots
            'dash_duration': 300,  # 300ms dashes
        }
        
        custom_encoder = BinaryEncoder(custom_config)
        binary_data = "0 1"
        timings = custom_encoder.binary_to_timing(binary_data)
        
        dot_duration, _ = timings[0]
        dash_duration, _ = timings[1]
        
        self.assertAlmostEqual(dot_duration, 0.1, places=2)   # 100ms
        self.assertAlmostEqual(dash_duration, 0.3, places=2)  # 300ms


if __name__ == '__main__':
    unittest.main()
