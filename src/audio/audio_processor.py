"""
Audio processing utilities for SonicVault.
"""

import numpy as np
from pydub import AudioSegment
from typing import List, Tuple

class AudioProcessor:
    """Utility class for audio processing operations."""
    
    @staticmethod
    def normalize_audio(samples: np.ndarray) -> np.ndarray:
        """Normalize audio samples to range [-1, 1]."""
        if np.max(np.abs(samples)) > 0:
            return samples / np.max(np.abs(samples))
        return samples
    
    @staticmethod
    def convert_to_mono(audio: AudioSegment) -> AudioSegment:
        """Convert audio to mono if it's stereo."""
        if audio.channels > 1:
            return audio.set_channels(1)
        return audio