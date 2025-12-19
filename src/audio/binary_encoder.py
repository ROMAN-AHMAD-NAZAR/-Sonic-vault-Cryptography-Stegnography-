"""
Binary Encoder for SonicVault
Converts Morse code to binary timing patterns and vice versa.
"""

import json
from typing import List, Tuple, Dict, Any

class BinaryEncoder:
    """
    Encodes binary data into timing patterns and decodes timing patterns back to binary.
    """
    
    # Default timing configuration (in milliseconds)
    DEFAULT_TIMING = {
        'dot_duration': 200,      # Duration of a dot in Morse
        'dash_duration': 600,     # Duration of a dash in Morse  
        'element_gap': 200,       # Gap between dots/dashes within a character
        'char_gap': 600,          # Gap between characters
        'word_gap': 1000,         # Gap between words
    }
    
    # Constants for binary representation
    DOT = '0'
    DASH = '1'
    CHAR_SEPARATOR = '/'
    WORD_SEPARATOR = '//'
    
    def __init__(self, timing_config: Dict[str, Any] = None):
        self.timing_config = self.DEFAULT_TIMING.copy()
        if timing_config:
            self.timing_config.update(timing_config)

    def morse_to_binary(self, morse_code: str) -> str:
        """
        Convert Morse code to binary representation.
        """
        if not morse_code:
            return ""
            
        binary_parts = []
        words = morse_code.split(' / ')  # Morse word separator
        
        for word in words:
            chars = word.split(' ')  # Morse character separator
            word_binary = []
            
            for morse_char in chars:
                if not morse_char:
                    continue
                    
                char_binary = []
                for element in morse_char:
                    if element == '.':
                        char_binary.append(self.DOT)
                    elif element == '-':
                        char_binary.append(self.DASH)
                if char_binary:
                    word_binary.append(''.join(char_binary))
            
            if word_binary:
                binary_parts.append(self.CHAR_SEPARATOR.join(word_binary))
        
        return self.WORD_SEPARATOR.join(binary_parts)

    def binary_to_morse(self, binary_data: str) -> str:
        """
        Convert binary representation back to Morse code.
        """
        if not binary_data:
            return ""
            
        morse_parts = []
        words = binary_data.split(self.WORD_SEPARATOR)
        
        for word in words:
            chars = word.split(self.CHAR_SEPARATOR)
            morse_chars = []
            
            for char_binary in chars:
                if not char_binary:
                    continue
                    
                morse_char = []
                for bit in char_binary:
                    if bit == self.DOT:
                        morse_char.append('.')
                    elif bit == self.DASH:
                        morse_char.append('-')
                if morse_char:
                    morse_chars.append(''.join(morse_char))
            
            if morse_chars:
                morse_parts.append(' '.join(morse_chars))
        
        return ' / '.join(morse_parts)

    def binary_to_timing(self, binary_data: str) -> List[Tuple[float, float]]:
        """
        Convert binary data to timing patterns for audio generation.
        """
        timing_patterns = []
        
        i = 0
        n = len(binary_data)
        
        while i < n:
            if binary_data[i:i+2] == self.WORD_SEPARATOR:
                # Word separator: add as gap after previous signal
                if timing_patterns:
                    last_signal, last_gap = timing_patterns[-1]
                    timing_patterns[-1] = (last_signal, last_gap + self.timing_config['word_gap'] / 1000.0)
                i += 2
                
            elif binary_data[i] == self.CHAR_SEPARATOR:
                # Character separator: add as gap after previous signal
                if timing_patterns:
                    last_signal, last_gap = timing_patterns[-1]
                    timing_patterns[-1] = (last_signal, last_gap + self.timing_config['char_gap'] / 1000.0)
                i += 1
                
            elif binary_data[i] == self.DOT:
                # Dot signal with element gap
                signal_dur = self.timing_config['dot_duration'] / 1000.0
                gap_dur = self.timing_config['element_gap'] / 1000.0
                timing_patterns.append((signal_dur, gap_dur))
                i += 1
                
            elif binary_data[i] == self.DASH:
                # Dash signal with element gap
                signal_dur = self.timing_config['dash_duration'] / 1000.0
                gap_dur = self.timing_config['element_gap'] / 1000.0
                timing_patterns.append((signal_dur, gap_dur))
                i += 1
                
            else:
                # Skip unknown characters
                i += 1
        
        # Remove gap after the last signal
        if timing_patterns:
            last_signal, last_gap = timing_patterns[-1]
            timing_patterns[-1] = (last_signal, 0.0)
        
        return timing_patterns

    def timing_to_binary(self, timings: List[Tuple[float, float]]) -> str:
        """
        Convert timing patterns back to binary with proper separator reconstruction.
        Detects gap durations to insert character and word separators.
        """
        if not timings:
            return ""
        
        # Get timing config in seconds
        dot_dur = self.timing_config['dot_duration'] / 1000.0
        dash_dur = self.timing_config['dash_duration'] / 1000.0
        element_gap = self.timing_config['element_gap'] / 1000.0
        char_gap = self.timing_config['char_gap'] / 1000.0
        word_gap = self.timing_config['word_gap'] / 1000.0
        
        # Thresholds for signal classification
        signal_threshold = (dot_dur + dash_dur) / 2.0
        
        # Gap thresholds - based on how gaps are accumulated in encoding:
        # - element_gap (0.2s): between elements in a character
        # - element_gap + char_gap (0.8s): between characters
        # - element_gap + word_gap (1.2s): between words (max)
        # Use midpoints to distinguish
        char_gap_threshold = (element_gap + (element_gap + char_gap)) / 2.0  # 0.5s
        word_gap_threshold = ((element_gap + char_gap) + (element_gap + word_gap)) / 2.0  # 1.0s
        
        binary_bits = []
        
        for i, (signal_duration, gap_duration) in enumerate(timings):
            # Handle signal: classify as dot or dash
            if signal_duration > 0:
                if signal_duration <= signal_threshold:
                    binary_bits.append(self.DOT)
                else:
                    binary_bits.append(self.DASH)
            
            # Handle gap: insert separators based on gap duration
            # Only insert separators between signals (not after the last one)
            if gap_duration > element_gap and i < len(timings) - 1:
                # Classify gap and insert appropriate separator
                if gap_duration > word_gap_threshold:
                    # Word separator (largest gap)
                    binary_bits.append(self.WORD_SEPARATOR)
                elif gap_duration > char_gap_threshold:
                    # Character separator (medium gap)
                    binary_bits.append(self.CHAR_SEPARATOR)
                # Note: element_gap (smallest gap) doesn't get a separator
        
        result = ''.join(binary_bits)
        print(f"   🔍 Binary Conversion: {len(result)} bits")
        return result

    def save_timing_config(self, filepath: str):
        """
        Save timing configuration to JSON file.
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.timing_config, f, indent=2)
        except Exception as e:
            raise Exception(f"Failed to save timing configuration: {e}")

    def load_timing_config(self, filepath: str):
        """
        Load timing configuration from JSON file.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
                if isinstance(cfg, dict):
                    self.timing_config.update(cfg)
                else:
                    raise ValueError("Configuration file must contain a dictionary")
        except Exception as e:
            raise Exception(f"Failed to load timing configuration: {e}")