#!/usr/bin/env python3
"""Debug script to analyze the encoded audio file."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.audio.audio_analyzer import AudioAnalyzer
from src.audio.binary_encoder import BinaryEncoder

# Analyze the audio file
analyzer = AudioAnalyzer()
timings = analyzer.analyze_timing_patterns_simple('test_short.wav')

print(f"Total timing patterns detected: {len(timings)}")
print(f"\nFirst 10 patterns (signal_duration, gap_duration):")
for i, (sig, gap) in enumerate(timings[:10]):
    print(f"  {i}: Signal={sig:.3f}s, Gap={gap:.3f}s")

print(f"\nLast 10 patterns:")
for i, (sig, gap) in enumerate(timings[-10:], start=len(timings)-10):
    print(f"  {i}: Signal={sig:.3f}s, Gap={gap:.3f}s")

# Convert to binary
encoder = BinaryEncoder()
binary = encoder.timing_to_binary(timings)
print(f"\nBinary data length: {len(binary)}")
print(f"Binary data (first 100 chars): {binary[:100]}")

# Expected: 285 binary digits
print(f"\nExpected: 285 patterns")
print(f"Got: {len(timings)} patterns")
print(f"Difference: {len(timings) - 285} patterns ({100*len(timings)/285:.1f}%)")
