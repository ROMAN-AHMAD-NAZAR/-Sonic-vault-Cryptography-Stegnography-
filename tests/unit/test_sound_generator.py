"""
Unit tests for sound generator.
"""

import unittest
import sys
import os
import tempfile

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from audio.sound_generator import SoundGenerator
from audio.binary_encoder import BinaryEncoder
from utils.morse_code import MorseCode

class TestSoundGenerator(unittest.TestCase):
    """Test cases for SoundGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sound_gen = SoundGenerator()
        self.encoder = BinaryEncoder()
        self.morse = MorseCode()
    
    def test_initialization(self):
        """Test sound generator initialization."""
        self.assertIsNotNone(self.sound_gen)
        self.assertEqual(self.sound_gen.current_theme, 'sine')
    
    def test_get_available_themes(self):
        """Test getting available themes."""
        themes = self.sound_gen.get_available_themes()
        expected_themes = ['sine', 'rain', 'birds', 'synth', 'digital']
        self.assertEqual(themes, expected_themes)
    
    def test_set_theme_valid(self):
        """Test setting valid theme."""
        self.sound_gen.set_theme('rain')
        self.assertEqual(self.sound_gen.current_theme, 'rain')
    
    def test_set_theme_invalid(self):
        """Test setting invalid theme."""
        with self.assertRaises(ValueError):
            self.sound_gen.set_theme('invalid_theme')
    
    def test_generate_silence(self):
        """Test silence generation."""
        silence = self.sound_gen.generate_silence(1.0)  # 1 second
        self.assertIsNotNone(silence)
        self.assertEqual(len(silence), 1000)  # 1000 ms
    
    def test_generate_sound_segments(self):
        """Test sound segment generation for different themes."""
        themes = self.sound_gen.get_available_themes()
        
        for theme in themes:
            with self.subTest(theme=theme):
                self.sound_gen.set_theme(theme)
                
                # Test dot sound
                dot_sound = self.sound_gen.generate_sound_segment(0.2, 'dot')
                self.assertIsNotNone(dot_sound)
                self.assertGreater(len(dot_sound), 0)
                
                # Test dash sound
                dash_sound = self.sound_gen.generate_sound_segment(0.6, 'dash')
                self.assertIsNotNone(dash_sound)
                self.assertGreater(len(dash_sound), 0)
    
    def test_timing_to_audio_basic(self):
        """Test basic timing to audio conversion."""
        # Simple timing: dot then dash
        timings = [
            (0.2, 0.2),  # dot
            (0.6, 0.2),  # dash
        ]
        
        audio = self.sound_gen.timing_to_audio(timings)
        self.assertIsNotNone(audio)
        self.assertGreater(len(audio), 0)
        
        # Calculate expected duration: (0.2 + 0.2) + (0.6 + 0.2) = 1.2 seconds
        expected_duration_ms = 1200
        self.assertAlmostEqual(len(audio), expected_duration_ms, delta=50)  # Allow 50ms tolerance
    
    def test_timing_to_audio_empty(self):
        """Test timing to audio with empty input."""
        audio = self.sound_gen.timing_to_audio([])
        self.assertIsNotNone(audio)
        self.assertEqual(len(audio), 1000)  # Default 1 second silence
    
    def test_save_audio(self):
        """Test audio file saving."""
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # Generate simple audio
            timings = [(0.1, 0.1)]
            audio = self.sound_gen.timing_to_audio(timings)
            
            # Save audio
            self.sound_gen.save_audio(audio, temp_path)
            
            # Check file exists and has content
            self.assertTrue(os.path.exists(temp_path))
            self.assertGreater(os.path.getsize(temp_path), 0)
            
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_full_pipeline(self):
        """Test full pipeline: text -> morse -> binary -> timing -> audio."""
        test_message = "SOS"
        
        # Convert to timing patterns
        morse_code = self.morse.text_to_morse(test_message)
        binary_data = self.encoder.morse_to_binary(morse_code)
        timings = self.encoder.binary_to_timing(binary_data)
        
        # Generate audio for each theme
        themes = self.sound_gen.get_available_themes()
        
        for theme in themes:
            with self.subTest(theme=theme):
                self.sound_gen.set_theme(theme)
                audio = self.sound_gen.timing_to_audio(timings)
                
                self.assertIsNotNone(audio)
                self.assertGreater(len(audio), 0)
    
    def test_generate_from_timing_and_save(self):
        """Test combined generation and saving."""
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            timings = [(0.1, 0.1), (0.2, 0.1)]
            audio = self.sound_gen.generate_from_timing_and_save(timings, temp_path)
            
            self.assertIsNotNone(audio)
            self.assertTrue(os.path.exists(temp_path))
            self.assertGreater(os.path.getsize(temp_path), 0)
            
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()
