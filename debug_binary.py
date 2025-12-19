#!/usr/bin/env python3
"""Debug script to check binary to timing conversion."""

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
binary_data = encoder.morse_to_binary(morse_code)

# Convert to timing
timings = encoder.binary_to_timing(binary_data)

print(f"Message: '{message}'")
print(f"Encrypted: '{encrypted}' ({len(encrypted)} chars)")
print(f"Morse code length: {len(morse_code)} chars")
print(f"Binary data length: {len(binary_data)} chars")
print(f"Number of timing patterns: {len(timings)}")
print()
print(f"First 10 timings:")
for i, (sig, gap) in enumerate(timings[:10]):
    print(f"  {i}: Signal={sig:.3f}s, Gap={gap:.3f}s")
