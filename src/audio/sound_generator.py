"""
Sound Generator for SonicVault
Generates audio files from timing patterns with different sound themes.
"""

import numpy as np
from scipy.io import wavfile
import os
from typing import List, Tuple
from pathlib import Path

class AudioSegment:
    """Simple audio segment class for compatibility."""
    
    def __init__(self, audio_array: np.ndarray, sample_rate: int = 44100):
        """
        Initialize audio segment.
        
        Args:
            audio_array: NumPy array of audio samples
            sample_rate: Sample rate in Hz
        """
        self.audio_array = audio_array
        self.sample_rate = sample_rate
        self.channels = 1 if len(audio_array.shape) == 1 else audio_array.shape[1]
    
    def __len__(self):
        """Get duration in milliseconds."""
        return int((len(self.audio_array) / self.sample_rate) * 1000)
    
    def __add__(self, other: 'AudioSegment') -> 'AudioSegment':
        """Concatenate two audio segments."""
        if self.sample_rate != other.sample_rate:
            raise ValueError("Sample rates must match")
        
        combined = np.concatenate([self.audio_array, other.audio_array])
        return AudioSegment(combined, self.sample_rate)
    
    def overlay(self, other: 'AudioSegment') -> 'AudioSegment':
        """Overlay two audio segments (mix them)."""
        if self.sample_rate != other.sample_rate:
            raise ValueError("Sample rates must match")
        
        # Pad the shorter one with zeros
        max_len = max(len(self.audio_array), len(other.audio_array))
        self_padded = np.pad(self.audio_array, (0, max_len - len(self.audio_array)))
        other_padded = np.pad(other.audio_array, (0, max_len - len(other.audio_array)))
        
        # Mix with equal volume
        mixed = (self_padded + other_padded) / 2
        
        # Normalize to avoid clipping
        max_val = np.max(np.abs(mixed))
        if max_val > 1.0:
            mixed = mixed / max_val * 0.95
        
        return AudioSegment(mixed, self.sample_rate)
    
    def export(self, filepath: str, format: str = 'wav'):
        """Export audio to file."""
        # Convert to int16
        audio_int16 = np.clip(self.audio_array * 32767, -32768, 32767).astype(np.int16)
        wavfile.write(filepath, self.sample_rate, audio_int16)


class SoundGenerator:
    """
    Generates audio from timing patterns with configurable sound themes.
    """
    
    # Audio configuration
    DEFAULT_CONFIG = {
        'sample_rate': 44100,
        'bit_depth': 16,
        'channels': 1,
        'base_frequency': 440,  # A4 note
        'amplitude': 0.8,
    }
    
    # Sound themes configuration
    THEMES = {
        'sine': {
            'description': 'Clean sine wave tones',
            'color': 'blue'
        },
        'rain': {
            'description': 'Raindrop-like sounds', 
            'color': 'gray'
        },
        'birds': {
            'description': 'Bird chirp sounds',
            'color': 'green'
        },
        'synth': {
            'description': 'Electronic synth tones',
            'color': 'purple'
        },
        'digital': {
            'description': 'Digital beep sounds',
            'color': 'orange'
        }
    }
    
    def __init__(self, config: dict = None):
        """
        Initialize the sound generator.
        
        Args:
            config (dict, optional): Audio configuration parameters
        """
        self.config = self.DEFAULT_CONFIG.copy()
        if config:
            self.config.update(config)
        
        self.current_theme = 'sine'
        self.sample_rate = self.config['sample_rate']
    
    def set_theme(self, theme: str):
        """
        Set the current sound theme.
        
        Args:
            theme (str): Theme name ('sine', 'rain', 'birds', 'synth', 'digital')
        """
        if theme not in self.THEMES:
            raise ValueError(f"Unknown theme: {theme}. Available: {list(self.THEMES.keys())}")
        self.current_theme = theme
    
    def get_available_themes(self) -> list:
        """
        Get list of available sound themes.
        
        Returns:
            list: Available theme names
        """
        return list(self.THEMES.keys())
    
    def _generate_sine_wave(self, frequency: float, duration_sec: float, amplitude: float = 0.8) -> np.ndarray:
        """Generate a sine wave."""
        t = np.linspace(0, duration_sec, int(self.sample_rate * duration_sec), False)
        return amplitude * np.sin(2 * np.pi * frequency * t)
    
    def _generate_noise(self, duration_sec: float, amplitude: float = 0.8) -> np.ndarray:
        """Generate white noise."""
        samples = int(self.sample_rate * duration_sec)
        return amplitude * np.random.randn(samples)
    
    def generate_sound_segment(self, duration: float, sound_type: str = 'dot') -> AudioSegment:
        """
        Generate a single sound segment based on current theme and sound type.
        
        Args:
            duration (float): Duration in seconds
            sound_type (str): Type of sound ('dot' or 'dash')
            
        Returns:
            AudioSegment: Generated audio segment
        """
        if self.current_theme == 'sine':
            audio = self._generate_sine_sound(duration, sound_type)
        elif self.current_theme == 'rain':
            audio = self._generate_rain_sound(duration, sound_type)
        elif self.current_theme == 'birds':
            audio = self._generate_bird_sound(duration, sound_type)
        elif self.current_theme == 'synth':
            audio = self._generate_synth_sound(duration, sound_type)
        elif self.current_theme == 'digital':
            audio = self._generate_digital_sound(duration, sound_type)
        else:
            audio = self._generate_sine_sound(duration, sound_type)
        
        return AudioSegment(audio, self.sample_rate)
    
    def _generate_sine_sound(self, duration_sec: float, sound_type: str) -> np.ndarray:
        """Generate sine wave sound."""
        if sound_type == 'dot':
            freq = self.config['base_frequency']
            amplitude = 0.6
        else:  # dash
            freq = self.config['base_frequency'] * 0.8  # Lower frequency for dashes
            amplitude = 0.6
        
        return self._generate_sine_wave(freq, duration_sec, amplitude)
    
    def _generate_rain_sound(self, duration_sec: float, sound_type: str) -> np.ndarray:
        """Generate raindrop-like sound."""
        if sound_type == 'dot':
            freq = self.config['base_frequency'] * 2
            tone = self._generate_sine_wave(freq, duration_sec, 0.4)
            noise = self._generate_noise(duration_sec, 0.2)
        else:
            freq = self.config['base_frequency'] * 1.5
            tone = self._generate_sine_wave(freq, duration_sec, 0.5)
            noise = self._generate_noise(duration_sec, 0.25)
        
        return tone + noise
    
    def _generate_bird_sound(self, duration_sec: float, sound_type: str) -> np.ndarray:
        """Generate bird chirp-like sound."""
        if sound_type == 'dot':
            freq = self.config['base_frequency'] * 3
            return self._generate_sine_wave(freq, duration_sec, 0.7)
        else:
            base_freq = self.config['base_frequency'] * 2.5
            # Create warble effect
            tone1 = self._generate_sine_wave(base_freq, duration_sec, 0.5)
            tone2 = self._generate_sine_wave(base_freq * 1.1, duration_sec, 0.4)
            return tone1 + tone2
    
    def _generate_synth_sound(self, duration_sec: float, sound_type: str) -> np.ndarray:
        """Generate electronic synth sound."""
        if sound_type == 'dot':
            freq = self.config['base_frequency']
        else:
            freq = self.config['base_frequency'] * 0.6
        
        # Add harmonics
        fundamental = self._generate_sine_wave(freq, duration_sec, 0.5)
        harmonic = self._generate_sine_wave(freq * 2, duration_sec, 0.3)
        return fundamental + harmonic
    
    def _generate_digital_sound(self, duration_sec: float, sound_type: str) -> np.ndarray:
        """Generate digital beep sound."""
        if sound_type == 'dot':
            freq = self.config['base_frequency'] * 1.5
        else:
            freq = self.config['base_frequency']
        
        return self._generate_sine_wave(freq, duration_sec, 0.7)
    
    def generate_silence(self, duration: float) -> AudioSegment:
        """
        Generate silence segment.
        
        Args:
            duration (float): Duration in seconds
            
        Returns:
            AudioSegment: Silence segment
        """
        silence = np.zeros(int(self.sample_rate * duration))
        return AudioSegment(silence, self.sample_rate)
    
    def timing_to_audio(self, timings: List[Tuple[float, float]]) -> AudioSegment:
        """
        Convert timing patterns to audio segments.
        
        Args:
            timings (List[Tuple]): List of (duration, gap) pairs in seconds
            
        Returns:
            AudioSegment: Combined audio file
        """
        audio_segments = []
        
        for i, (duration, gap) in enumerate(timings):
            # Generate sound for signal duration (if any)
            if duration > 0:
                # Determine if this is likely a dot or dash based on duration
                dot_max = 0.3  # 300ms
                if duration <= dot_max:
                    sound_segment = self.generate_sound_segment(duration, 'dot')
                else:
                    sound_segment = self.generate_sound_segment(duration, 'dash')
                audio_segments.append(sound_segment)
            
            # Add gap after signal
            if gap > 0:
                silence_segment = self.generate_silence(gap)
                audio_segments.append(silence_segment)
        
        # Combine all segments
        if not audio_segments:
            return self.generate_silence(1.0)  # 1 second silence if empty
        
        combined_audio = audio_segments[0]
        for segment in audio_segments[1:]:
            combined_audio = combined_audio + segment
        
        return combined_audio
    
    def save_audio(self, audio: AudioSegment, filepath: str):
        """
        Save audio to file.
        
        Args:
            audio (AudioSegment): Audio to save
            filepath (str): Output file path
        """
        # Ensure directory exists
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        # Export as WAV
        audio.export(filepath, format='wav')
    
    def generate_from_timing_and_save(self, timings: List[Tuple[float, float]], filepath: str):
        """
        Generate audio from timing patterns and save to file.
        
        Args:
            timings (List[Tuple]): Timing patterns
            filepath (str): Output file path
        """
        audio = self.timing_to_audio(timings)
        self.save_audio(audio, filepath)
        return audio


# Example usage and testing
if __name__ == "__main__":
    from binary_encoder import BinaryEncoder
    from utils.morse_code import MorseCode
    
    # Create instances
    morse = MorseCode()
    encoder = BinaryEncoder()
    sound_gen = SoundGenerator()
    
    # Test message
    test_message = "SOS"
    
    print("Sound Generator Test")
    print("=" * 50)
    print(f"Testing with message: '{test_message}'")
    print(f"Available themes: {sound_gen.get_available_themes()}")
    print()
    
    try:
        # Convert to timing patterns
        morse_code = morse.text_to_morse(test_message)
        binary_data = encoder.morse_to_binary(morse_code)
        timings = encoder.binary_to_timing(binary_data)
        
        print(f"Morse: {morse_code}")
        print(f"Binary: {binary_data}")
        print(f"Timing patterns: {len(timings)}")
        print()
        
        # Test each theme
        for theme in sound_gen.get_available_themes():
            sound_gen.set_theme(theme)
            output_file = f"test_output_{theme}.wav"
            
            # Generate audio
            audio = sound_gen.generate_from_timing_and_save(timings, output_file)
            
            print(f"Theme: {theme:8} | Duration: {len(audio)/1000:.2f}s | File: {output_file}")
            
        print()
        print("All test files generated successfully!")
        print("Play the generated WAV files to hear the different sound themes.")
        
    except Exception as e:
        print(f"Error during sound generation: {e}")
    """
    Generates audio from timing patterns with configurable sound themes.
    """
    
    # Audio configuration
    DEFAULT_CONFIG = {
        'sample_rate': 44100,
        'bit_depth': 16,
        'channels': 1,
        'base_frequency': 440,  # A4 note
        'amplitude': 0.8,
    }
    
    # Sound themes configuration
    THEMES = {
        'sine': {
            'description': 'Clean sine wave tones',
            'color': 'blue'
        },
        'rain': {
            'description': 'Raindrop-like sounds', 
            'color': 'gray'
        },
        'birds': {
            'description': 'Bird chirp sounds',
            'color': 'green'
        },
        'synth': {
            'description': 'Electronic synth tones',
            'color': 'purple'
        },
        'digital': {
            'description': 'Digital beep sounds',
            'color': 'orange'
        }
    }
    
    def __init__(self, config: dict = None):
        """
        Initialize the sound generator.
        
        Args:
            config (dict, optional): Audio configuration parameters
        """
        self.config = self.DEFAULT_CONFIG.copy()
        if config:
            self.config.update(config)
        
        self.current_theme = 'sine'
    
    def set_theme(self, theme: str):
        """
        Set the current sound theme.
        
        Args:
            theme (str): Theme name ('sine', 'rain', 'birds', 'synth', 'digital')
        """
        if theme not in self.THEMES:
            raise ValueError(f"Unknown theme: {theme}. Available: {list(self.THEMES.keys())}")
        self.current_theme = theme
    
    def get_available_themes(self) -> list:
        """
        Get list of available sound themes.
        
        Returns:
            list: Available theme names
        """
        return list(self.THEMES.keys())
    
    
    def generate_sound_segment(self, duration: float, sound_type: str = 'dot') -> AudioSegment:
        """
        Generate a single sound segment based on current theme and sound type.
        
        Args:
            duration (float): Duration in seconds
            sound_type (str): Type of sound ('dot' or 'dash')
            
        Returns:
            AudioSegment: Generated audio segment
        """
        if self.current_theme == 'sine':
            audio = self._generate_sine_sound(duration, sound_type)
        elif self.current_theme == 'rain':
            audio = self._generate_rain_sound(duration, sound_type)
        elif self.current_theme == 'birds':
            audio = self._generate_bird_sound(duration, sound_type)
        elif self.current_theme == 'synth':
            audio = self._generate_synth_sound(duration, sound_type)
        elif self.current_theme == 'digital':
            audio = self._generate_digital_sound(duration, sound_type)
        else:
            audio = self._generate_sine_sound(duration, sound_type)
        
        return AudioSegment(audio, self.sample_rate)
    
    
    def _generate_sine_sound(self, duration_sec: float, sound_type: str) -> np.ndarray:
        """Generate sine wave sound."""
        if sound_type == 'dot':
            freq = self.config['base_frequency']
            amplitude = 0.6
        else:  # dash
            freq = self.config['base_frequency'] * 0.8  # Lower frequency for dashes
            amplitude = 0.6
        
        return self._generate_sine_wave(freq, duration_sec, amplitude)
    
    def _generate_rain_sound(self, duration_sec: float, sound_type: str) -> np.ndarray:
        """Generate raindrop-like sound."""
        if sound_type == 'dot':
            freq = self.config['base_frequency'] * 2
            tone = self._generate_sine_wave(freq, duration_sec, 0.4)
            noise = self._generate_noise(duration_sec, 0.2)
        else:
            freq = self.config['base_frequency'] * 1.5
            tone = self._generate_sine_wave(freq, duration_sec, 0.5)
            noise = self._generate_noise(duration_sec, 0.25)
        
        return tone + noise
    
    def _generate_bird_sound(self, duration_sec: float, sound_type: str) -> np.ndarray:
        """Generate bird chirp-like sound."""
        if sound_type == 'dot':
            freq = self.config['base_frequency'] * 3
            return self._generate_sine_wave(freq, duration_sec, 0.7)
        else:
            base_freq = self.config['base_frequency'] * 2.5
            # Create warble effect
            tone1 = self._generate_sine_wave(base_freq, duration_sec, 0.5)
            tone2 = self._generate_sine_wave(base_freq * 1.1, duration_sec, 0.4)
            return tone1 + tone2
    
    def _generate_synth_sound(self, duration_sec: float, sound_type: str) -> np.ndarray:
        """Generate electronic synth sound."""
        if sound_type == 'dot':
            freq = self.config['base_frequency']
        else:
            freq = self.config['base_frequency'] * 0.6
        
        # Add harmonics
        fundamental = self._generate_sine_wave(freq, duration_sec, 0.5)
        harmonic = self._generate_sine_wave(freq * 2, duration_sec, 0.3)
        return fundamental + harmonic
    
    def _generate_digital_sound(self, duration_sec: float, sound_type: str) -> np.ndarray:
        """Generate digital beep sound."""
        if sound_type == 'dot':
            freq = self.config['base_frequency'] * 1.5
        else:
            freq = self.config['base_frequency']
        
        return self._generate_sine_wave(freq, duration_sec, 0.7)
    
    
    def generate_silence(self, duration: float) -> AudioSegment:
        """
        Generate silence segment.
        
        Args:
            duration (float): Duration in seconds
            
        Returns:
            AudioSegment: Silence segment
        """
        silence = np.zeros(int(self.sample_rate * duration))
        return AudioSegment(silence, self.sample_rate)
    
    def timing_to_audio(self, timings: List[Tuple[float, float]]) -> AudioSegment:
        """
        Convert timing patterns to audio segments.
        
        Args:
            timings (List[Tuple]): List of (duration, gap) pairs in seconds
            
        Returns:
            AudioSegment: Combined audio file
        """
        audio_segments = []
        
        for i, (duration, gap) in enumerate(timings):
            # Generate sound for signal duration (if any)
            if duration > 0:
                # Determine if this is likely a dot or dash based on duration
                dot_max = 0.3  # 300ms
                if duration <= dot_max:
                    sound_segment = self.generate_sound_segment(duration, 'dot')
                else:
                    sound_segment = self.generate_sound_segment(duration, 'dash')
                audio_segments.append(sound_segment)
            
            # Add gap after signal
            if gap > 0:
                silence_segment = self.generate_silence(gap)
                audio_segments.append(silence_segment)
        
        # Combine all segments
        if not audio_segments:
            return self.generate_silence(1.0)  # 1 second silence if empty
        
        combined_audio = audio_segments[0]
        for segment in audio_segments[1:]:
            combined_audio = combined_audio + segment
        
        return combined_audio
    
    def save_audio(self, audio: AudioSegment, filepath: str):
        """
        Save audio to file.
        
        Args:
            audio (AudioSegment): Audio to save
            filepath (str): Output file path
        """
        # Ensure directory exists
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        # Export as WAV
        audio.export(filepath, format='wav')
    
    def generate_from_timing_and_save(self, timings: List[Tuple[float, float]], filepath: str):
        """
        Generate audio from timing patterns and save to file.
        
        Args:
            timings (List[Tuple]): Timing patterns
            filepath (str): Output file path
        """
        audio = self.timing_to_audio(timings)
        self.save_audio(audio, filepath)
        return audio


# Example usage and testing
if __name__ == "__main__":
    from binary_encoder import BinaryEncoder
    from utils.morse_code import MorseCode
    
    # Create instances
    morse = MorseCode()
    encoder = BinaryEncoder()
    sound_gen = SoundGenerator()
    
    # Test message
    test_message = "SOS"
    
    print("Sound Generator Test")
    print("=" * 50)
    print(f"Testing with message: '{test_message}'")
    print(f"Available themes: {sound_gen.get_available_themes()}")
    print()
    
    try:
        # Convert to timing patterns
        morse_code = morse.text_to_morse(test_message)
        binary_data = encoder.morse_to_binary(morse_code)
        timings = encoder.binary_to_timing(binary_data)
        
        print(f"Morse: {morse_code}")
        print(f"Binary: {binary_data}")
        print(f"Timing patterns: {len(timings)}")
        print()
        
        # Test each theme
        for theme in sound_gen.get_available_themes():
            sound_gen.set_theme(theme)
            output_file = f"test_output_{theme}.wav"
            
            # Generate audio
            audio = sound_gen.generate_from_timing_and_save(timings, output_file)
            
            print(f"Theme: {theme:8} | Duration: {len(audio)/1000:.2f}s | File: {output_file}")
            
        print()
        print("All test files generated successfully!")
        print("Play the generated WAV files to hear the different sound themes.")
        
    except Exception as e:
        print(f"Error during sound generation: {e}")
