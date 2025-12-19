"""
Audio utility functions for SonicVault.
"""

def validate_audio_file(file_path: str) -> bool:
    """Validate that file exists and is a supported audio format."""
    import os
    supported_formats = {'.wav', '.mp3', '.flac', '.ogg', '.m4a'}
    return os.path.exists(file_path) and any(file_path.lower().endswith(fmt) for fmt in supported_formats)