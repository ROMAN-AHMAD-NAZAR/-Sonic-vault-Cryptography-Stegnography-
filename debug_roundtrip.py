#!/usr/bin/env python3
"""Debug round-trip binary to timing to binary conversion."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.audio.binary_encoder import BinaryEncoder
from src.utils.morse_code import MorseCode
from src.crypto.aes_manager import AESManager

# Encrypt a message
aes = AESManager()
message = "Hi"
password = "MyPass123"
encrypted = aes.encrypt_to_string(message, password)

# Convert to Morse and binary
morse = MorseCode()
morse_code = morse.text_to_morse(encrypted)

encoder = BinaryEncoder()
binary_original = encoder.morse_to_binary(morse_code)

# Convert to timing
timings = encoder.binary_to_timing(binary_original)

# Convert back to binary
binary_recovered = encoder.timing_to_binary(timings)

print(f"Original binary: {len(binary_original)} bits")
print(f"Original (first 100): {binary_original[:100]}")
print()
print(f"Timing patterns: {len(timings)}")
print(f"First 5 timings: {timings[:5]}")
print()
print(f"Recovered binary: {len(binary_recovered)} bits")
print(f"Recovered (first 100): {binary_recovered[:100]}")
print()
print(f"Match: {binary_original == binary_recovered}")
if binary_original != binary_recovered:
    print(f"Difference at position: {next((i for i in range(min(len(binary_original), len(binary_recovered))) if binary_original[i] != binary_recovered[i]), -1)}")
