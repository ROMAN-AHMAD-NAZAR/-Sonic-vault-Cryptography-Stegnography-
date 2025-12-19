"""
Audio Analyzer for SonicVault
Analyzes audio files to extract timing patterns for decoding.
"""

import numpy as np
from pydub import AudioSegment
from typing import List, Tuple, Dict, Any

class AudioAnalyzer:
    """
    Analyzes audio files to detect timing patterns of Morse code signals.
    """
    
    def __init__(self, sample_rate: int = 44100):
        """
        Initialize the audio analyzer.
        """
        self.sample_rate = sample_rate
    
    def analyze_timing_patterns_simple(self, audio_file: str) -> List[Tuple[float, float]]:
        """
        SIMPLE AND ROBUST timing pattern analysis.
        """
        try:
            # Load audio file
            audio = AudioSegment.from_file(audio_file)
            
            # Convert to mono and set sample rate
            audio = audio.set_channels(1).set_frame_rate(self.sample_rate)
            
            # Convert to numpy array
            samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
            samples = samples / (2**15)  # Normalize for 16-bit audio
            
            return self._detect_timing_patterns_fixed(samples)
            
        except Exception as e:
            raise Exception(f"Audio analysis failed: {e}")
    
    def analyze_timing_patterns_robust(self, audio_file: str) -> List[Tuple[float, float]]:
        """
        Use simple method for now - it's more reliable.
        """
        return self.analyze_timing_patterns_simple(audio_file)
    
    def _detect_timing_patterns_fixed(self, samples: np.ndarray) -> List[Tuple[float, float]]:
        """
        FIXED: Much simpler and more reliable timing detection.
        """
        if len(samples) == 0:
            return []

        # Use larger frames for stability (100ms)
        frame_length = int(0.1 * self.sample_rate)  # 100ms frames
        frame_duration = frame_length / self.sample_rate
        
        # Calculate frame energy
        frame_energy = []
        for i in range(0, len(samples), frame_length):
            frame = samples[i:i + frame_length]
            if len(frame) > 0:
                energy = np.sqrt(np.mean(frame**2))
                frame_energy.append(energy)
        
        if not frame_energy:
            return []
        
        # Use fixed threshold based on maximum amplitude
        max_energy = np.max(frame_energy)
        energy_threshold = max_energy * 0.2  # 20% of peak - much more conservative
        
        # Simple state detection
        is_signal = [energy > energy_threshold for energy in frame_energy]
        
        # Group consecutive states
        timing_patterns = []
        current_state = is_signal[0]
        current_duration = 1
        
        for i in range(1, len(is_signal)):
            if is_signal[i] == current_state:
                current_duration += 1
            else:
                # State change - only add if it meets minimum duration
                duration_seconds = current_duration * frame_duration
                
                if current_state:  # Signal ended
                    # Only add signals that are at least 150ms (dot is 200ms)
                    if duration_seconds >= 0.15:
                        timing_patterns.append((duration_seconds, 0.0))
                else:  # Silence ended
                    # Only add gaps that are at least 100ms and we have a previous signal
                    if duration_seconds >= 0.1 and timing_patterns:
                        last_signal, last_gap = timing_patterns[-1]
                        timing_patterns[-1] = (last_signal, duration_seconds)
                
                current_state = is_signal[i]
                current_duration = 1
        
        # Handle final segment
        if current_duration > 0:
            duration_seconds = current_duration * frame_duration
            if current_state and duration_seconds >= 0.15:
                timing_patterns.append((duration_seconds, 0.0))
            elif not current_state and duration_seconds >= 0.1 and timing_patterns:
                last_signal, last_gap = timing_patterns[-1]
                timing_patterns[-1] = (last_signal, duration_seconds)
        
        print(f"   🔍 Audio Analysis: {len(timing_patterns)} patterns found")
        return timing_patterns

    def analyze_audio_quality(self, audio_file: str) -> Dict[str, Any]:
        """
        Analyze audio file quality.
        """
        try:
            audio = AudioSegment.from_file(audio_file)
            samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
            samples = samples / (2**15)
            
            return {
                'duration_seconds': len(audio) / 1000.0,
                'sample_rate': audio.frame_rate,
                'channels': audio.channels,
                'max_amplitude': float(np.max(np.abs(samples))),
            }
        except Exception as e:
            return {'error': str(e)}