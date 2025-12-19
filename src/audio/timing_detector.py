"""
Timing pattern detector from audio (legacy - use AudioAnalyzer instead).
"""

import warnings
from typing import List

class TimingDetector:
    """Legacy timing detector - use AudioAnalyzer for new code."""

    def detect(self, audio_data: bytes) -> List:
        """
        Legacy detection method.
        
        Args:
            audio_data: Audio data in bytes
            
        Returns:
            Empty list (placeholder)
        """
        warnings.warn("TimingDetector is deprecated. Use AudioAnalyzer instead.", DeprecationWarning)
        return []   