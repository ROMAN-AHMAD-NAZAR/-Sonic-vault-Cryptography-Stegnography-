
import os
import sys
import base64
from pathlib import Path
from typing import Tuple, Optional
from datetime import datetime
import warnings
# In your sonic_vault.py imports section, ensure you have:
from audio.audio_analyzer import AudioAnalyzer
# Suppress pydub warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pydub")

# Ensure src is in path for imports
_src_path = Path(__file__).parent.parent
if str(_src_path) not in sys.path:
    sys.path.insert(0, str(_src_path))

from crypto.aes_manager import AESManager
from crypto.dsa_manager import DSAManager
from audio.binary_encoder import BinaryEncoder
from audio.sound_generator import SoundGenerator
from audio.audio_analyzer import AudioAnalyzer
from utils.morse_code import MorseCode
from utils.validation import validate_nonempty

class SonicVault:
    """
    Main application class for SonicVault - Secure Audio Steganography.
    """
    
    def __init__(self, config: dict = None):
        """
        Initialize SonicVault with all components.
        
        Args:
            config (dict, optional): Configuration parameters
        """
        self.config = config or {}
        
        # Initialize all components
        self.aes = AESManager()
        self.dsa = DSAManager()
        self.morse = MorseCode()
        self.encoder = BinaryEncoder()
        self.sound_gen = SoundGenerator()
        
        # Default file paths
        self.default_private_key = "sonic_vault_private.pem"
        self.default_public_key = "sonic_vault_public.pem"
    
    def encode_message(self, message: str, password: str, output_file: str, 
                      theme: str = "sine", sign: bool = True, 
                      private_key_path: str = None) -> dict:
        """
        Encode a secure message into an audio file.
        """
        print("🔐 SonicVault - Encoding Secure Message")
        print("=" * 50)
        print(f"📝 Message: '{message}'")
        print(f"🎯 Output: {output_file}")
        print(f"🎵 Theme: {theme}")
        print(f"📝 Signed: {sign}")
        print()
        
        # Validate inputs
        validate_nonempty(message, "message")
        validate_nonempty(password, "password")
        validate_nonempty(output_file, "output_file")
        
        # Set sound theme
        if theme not in self.sound_gen.get_available_themes():
            raise ValueError(f"Invalid theme: {theme}. Available: {self.sound_gen.get_available_themes()}")
        self.sound_gen.set_theme(theme)
        
        # Step 1: Encrypt the message
        print("🔄 Step 1/5: Encrypting message with AES-256...")
        encrypted_data = self.aes.encrypt_to_string(message, password)
        print(f"   ✅ Encrypted data: {len(encrypted_data)} bytes")
        
        # Step 2: Add digital signature if requested
        if sign:
            print("🔄 Step 2/5: Adding digital signature with DSA-2048...")
            if private_key_path and os.path.exists(private_key_path):
                # Load existing private key
                with open(private_key_path, 'rb') as f:
                    private_key = self.dsa.private_key_from_bytes(f.read())
                print(f"   ✅ Loaded existing private key: {private_key_path}")
            else:
                # Generate new key pair
                print("   🔑 Generating new DSA key pair...")
                private_key, public_key = self.dsa.generate_keypair()
                
                # Save keys
                private_key_path = private_key_path or self.default_private_key
                public_key_path = private_key_path.replace('_private.pem', '_public.pem') if '_private.pem' in private_key_path else self.default_public_key
                
                self.dsa.save_keypair(private_key, public_key, private_key_path, public_key_path)
                print(f"   💾 New keys saved: {private_key_path}, {public_key_path}")
            
            # Sign the encrypted data
            signature = self.dsa.sign_data(encrypted_data.encode('utf-8'), private_key)
            signed_data = encrypted_data + "|SIG|" + base64.b64encode(signature).decode('utf-8')
            print(f"   ✅ Signature added: {len(signature)} bytes")
        else:
            signed_data = encrypted_data
            print("   ⚠️  Skipping digital signature")
        
        # Step 3: Convert to Morse code
        print("🔄 Step 3/5: Converting to Morse code...")
        payload_hex = signed_data.encode('utf-8').hex().upper()
        morse_code = self.morse.text_to_morse(payload_hex)
        print(f"   ✅ Morse code: {len(morse_code.split())} elements")
        
        # Step 4: Convert to binary with timing patterns
        print("🔄 Step 4/5: Converting to binary timing patterns...")
        binary_data = self.encoder.morse_to_binary(morse_code)
        timings = self.encoder.binary_to_timing(binary_data)
        print(f"   ✅ Binary data: {len(binary_data)} bits")
        print(f"   ✅ Timing patterns: {len(timings)} segments")
        
        # Step 5: Generate audio file
        print("🔄 Step 5/5: Generating audio file...")
        audio = self.sound_gen.timing_to_audio(timings)
        self.sound_gen.save_audio(audio, output_file)
        print(f"   ✅ Audio file created: {len(audio)/1000:.2f} seconds")
        
        # Return results
        print("\n" + "=" * 50)
        print("✅ ENCODING COMPLETE!")
        print("=" * 50)
        return {
            'success': True,
            'output_file': output_file,
            'message_length': len(message),
            'encrypted_length': len(encrypted_data),
            'audio_duration_seconds': len(audio) / 1000.0,
            'theme': theme,
            'signed': sign,
            'private_key_path': private_key_path if sign else None,
            'timestamp': datetime.now().isoformat()
        }
    
    def decode_message(self, audio_file: str, password: str, public_key_path: str = None) -> dict:
        """
        Decode a message from an audio file.
        """
        print("🔐 SonicVault - Decoding Secure Message")
        print("=" * 50)
        print(f"🎵 Input: {audio_file}")
        print()
        
        # Validate inputs
        validate_nonempty(audio_file, "audio_file")
        validate_nonempty(password, "password")
        
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        
        # Step 1: Analyze audio to extract timing patterns
        print("🔄 Step 1/6: Analyzing audio file...")
        analyzer = AudioAnalyzer()
        try:
            # BUG FIX 1: Use improved timing pattern detection with better threshold
            timings = analyzer.analyze_timing_patterns_robust(audio_file)
            if not timings:
                # Fallback to simple method if robust method fails
                timings = analyzer.analyze_timing_patterns_simple(audio_file)
            
            print(f"   📊 Analyzed {len(timings)} valid timing patterns")
            
            # BUG FIX 2: Validate we have enough timing patterns
            if len(timings) < 10:
                raise ValueError(f"Insufficient timing patterns detected: {len(timings)}")
                
        except Exception as e:
            print(f"   ❌ Audio analysis failed: {e}")
            return {
                'success': False,
                'message': f"Audio analysis failed: {e}",
                'timestamp': datetime.now().isoformat()
            }
        
        # Step 2: Convert timing patterns to binary
        print("🔄 Step 2/6: Converting timing patterns to binary...")
        try:
            binary_data = self.encoder.timing_to_binary(timings)
            print(f"   ✅ Binary data: {len(binary_data)} bits")
            
            # BUG FIX 3: Validate binary data length
            if len(binary_data) < 20:
                raise ValueError(f"Binary data too short: {len(binary_data)} bits")
                
        except Exception as e:
            print(f"   ❌ Binary conversion failed: {e}")
            return {
                'success': False,
                'message': f"Binary conversion failed: {e}",
                'timestamp': datetime.now().isoformat()
            }
        
        # Step 3: Convert binary to Morse code
        print("🔄 Step 3/6: Converting binary to Morse code...")
        try:
            morse_code = self.encoder.binary_to_morse(binary_data)
            print(f"   ✅ Morse code extracted: {len(morse_code)} characters")
            
            # BUG FIX 4: Validate Morse code
            if len(morse_code) < 10:
                raise ValueError(f"Morse code too short: {len(morse_code)} chars")
                
        except Exception as e:
            print(f"   ❌ Morse conversion failed: {e}")
            return {
                'success': False,
                'message': f"Morse conversion failed: {e}",
                'timestamp': datetime.now().isoformat()
            }
        
        # Step 4: Convert Morse code to text
        print("🔄 Step 4/6: Converting Morse code to text...")
        try:
            # Use error-resilient Morse decoding
            extracted_hex = self.morse.morse_to_text(morse_code, skip_errors=True)
            if len(extracted_hex) < 2:
                print(f"   ⚠️  Warning: Extracted data seems short: {len(extracted_hex)} chars")
            extracted_bytes = bytes.fromhex(extracted_hex)
            extracted_data = extracted_bytes.decode('utf-8')
            print(f"   ✅ Extracted data: {len(extracted_data)} characters")

        except Exception as e:
            print(f"   ❌ Text conversion failed: {e}")
            return {
                'success': False,
                'message': f"Text conversion failed: {e}",
                'timestamp': datetime.now().isoformat()
            }
        # Step 5: Handle signature and decryption
        signature_valid = None
        encrypted_data = extracted_data
        
        if "|SIG|" in extracted_data:
            print("🔄 Step 5/6: Verifying digital signature...")
            try:
                encrypted_data, signature_b64 = extracted_data.split("|SIG|")
                signature = base64.b64decode(signature_b64)
                
                # Verify signature
                if public_key_path and os.path.exists(public_key_path):
                    with open(public_key_path, 'rb') as f:
                        public_key = self.dsa.public_key_from_bytes(f.read())
                    
                    signature_valid = self.dsa.verify_signature(
                        encrypted_data.encode('utf-8'), 
                        signature, 
                        public_key
                    )
                    status = "✅ VALID" if signature_valid else "❌ INVALID"
                    print(f"   {status} Digital signature verified")
                else:
                    signature_valid = False
                    print("   ⚠️  No public key provided for signature verification")
                    
            except Exception as e:
                print(f"   ❌ Signature verification failed: {e}")
                signature_valid = False
        else:
            encrypted_data = extracted_data
            signature_valid = None
            print("   ℹ️  No signature found in message")
        
        # Step 6: Decrypt the message
        print("🔄 Step 6/6: Decrypting message...")
        try:
            # BUG FIX 6: Add validation before decryption
            if not encrypted_data or len(encrypted_data) < 16:
                raise ValueError("Encrypted data too short or empty")
                
            decrypted_message = self.aes.decrypt_from_string(encrypted_data, password)
            decryption_success = True
            print("   ✅ Decryption successful!")
            
        except ValueError as e:
            decrypted_message = f"Decryption failed: {e}"
            decryption_success = False
            print(f"   ❌ Decryption failed: {e}")
        except Exception as e:
            decrypted_message = f"Unexpected error during decryption: {e}"
            decryption_success = False
            print(f"   ❌ Decryption error: {e}")
        
        # Return results
        print("\n" + "=" * 50)
        if decryption_success and (signature_valid is not False):
            print("✅ DECODING SUCCESSFUL!")
            print(f"💬 Original message: '{decrypted_message}'")
        else:
            print("❌ DECODING FAILED!")
            if not decryption_success:
                print(f"💬 Error: {decrypted_message}")
            elif signature_valid is False:
                print(f"💬 Error: Digital signature verification failed")
        print("=" * 50)
        
        return {
            'success': decryption_success and (signature_valid is not False),
            'message': decrypted_message,
            'signature_valid': signature_valid,
            'timing_patterns_count': len(timings),
            'binary_data_length': len(binary_data),
            'extracted_data_length': len(extracted_data),
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_keypair(self, private_key_path: str = None, public_key_path: str = None,
                        password: str = None) -> dict:
        """
        Generate a new DSA key pair.
        
        Args:
            private_key_path (str): Path for private key file
            public_key_path (str): Path for public key file
            password (str): Password for private key encryption
            
        Returns:
            dict: Key generation results
        """
        print("🔑 Generating DSA key pair...")
        private_key, public_key = self.dsa.generate_keypair()
        
        # Set default paths if not provided
        private_key_path = private_key_path or self.default_private_key
        public_key_path = public_key_path or self.default_public_key
        
        # Save keys
        self.dsa.save_keypair(private_key, public_key, private_key_path, public_key_path, password)
        
        return {
            'success': True,
            'private_key_path': private_key_path,
            'public_key_path': public_key_path,
            'key_size': 2048,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_audio_themes(self) -> list:
        """
        Get available audio themes.
        
        Returns:
            list: Available theme names
        """
        return self.sound_gen.get_available_themes()
    
    def validate_password(self, password: str) -> Tuple[bool, str]:
        """
        Validate password strength.
        
        Args:
            password (str): Password to validate
            
        Returns:
            Tuple[bool, str]: (is_valid, message)
        """
        return self.aes.validate_password_strength(password)
    
    def get_system_info(self) -> dict:
        """
        Get system information and capabilities.
        
        Returns:
            dict: System information
        """
        return {
            'version': '1.0.0',
            'components': {
                'aes_encryption': 'AES-256-CBC with PBKDF2',
                'dsa_signatures': 'DSA-2048 with SHA-256',
                'audio_themes': self.get_audio_themes(),
                'morse_support': len(self.morse.get_supported_characters()),
            },
            'default_key_paths': {
                'private_key': self.default_private_key,
                'public_key': self.default_public_key,
            }
        }
    
    def run(self) -> str:
        """
        Simple status check method for testing.
        
        Returns:
            str: Status indicator
        """
        return "running"


# Example usage and testing
if __name__ == "__main__":
    vault = SonicVault()
    
    print("SonicVault - Secure Audio Steganography")
    print("=" * 50)
    
    # Display system info
    info = vault.get_system_info()
    print(f"Version: {info['version']}")
    print(f"Audio Themes: {', '.join(info['components']['audio_themes'])}")
    print(f"Morse Support: {info['components']['morse_support']} characters")
    print()
    
    # Test message
    test_message = "Hello from SonicVault! This is a secret message."
    test_password = "MyStrongPassword123!"
    output_file = "test_encoded_message.wav"
    
    print("Testing Encoding Pipeline:")
    print("-" * 30)
    
    try:
        # Encode message
        encode_result = vault.encode_message(
            message=test_message,
            password=test_password,
            output_file=output_file,
            theme="sine",
            sign=True
        )
        
        print(f"✓ Message encoded successfully!")
        print(f"  Output: {encode_result['output_file']}")
        print(f"  Duration: {encode_result['audio_duration_seconds']:.2f}s")
        print(f"  Theme: {encode_result['theme']}")
        print(f"  Signed: {encode_result['signed']}")
        print()
        
        # Test password validation
        is_valid, msg = vault.validate_password(test_password)
        print(f"Password validation: {msg}")
        print()
        
        # Display available themes
        themes = vault.get_audio_themes()
        print(f"Available audio themes: {', '.join(themes)}")
        
    except Exception as e:
        print(f"❌ Error during encoding: {e}")