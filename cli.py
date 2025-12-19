#!/usr/bin/env python3
"""
SonicVault CLI - Command Line Interface for Secure Audio Steganography
"""

import argparse
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.sonic_vault import SonicVault
from crypto.aes_manager import AESManager
from crypto.dsa_manager import DSAManager

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="SonicVault - Secure Audio Steganography",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Encode a secret message
  python cli.py encode "Meet at midnight" secret.wav --password MyPass123 --theme rain

  # Decode a message
  python cli.py decode secret.wav --password MyPass123

  # Generate encryption keys
  python cli.py generate-keys --output my_keys

  # Get system info
  python cli.py info
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Encode command
    encode_parser = subparsers.add_parser('encode', help='Encode a message into audio')
    encode_parser.add_argument('message', help='Message to encode')
    encode_parser.add_argument('output', help='Output audio file path')
    encode_parser.add_argument('--password', '-p', required=True, help='Encryption password')
    encode_parser.add_argument('--theme', '-t', default='sine', 
                              choices=['sine', 'rain', 'birds', 'synth', 'digital'],
                              help='Sound theme (default: sine)')
    encode_parser.add_argument('--sign', '-s', action='store_true', 
                              help='Add digital signature')
    encode_parser.add_argument('--private-key', '-k', 
                              help='Private key file for signing')
    
    # Decode command  
    decode_parser = subparsers.add_parser('decode', help='Decode a message from audio')
    decode_parser.add_argument('input', help='Input audio file path')
    decode_parser.add_argument('--password', '-p', required=True, help='Decryption password')
    decode_parser.add_argument('--public-key', '-k', 
                              help='Public key file for signature verification')
    
    # Generate keys command
    keys_parser = subparsers.add_parser('generate-keys', help='Generate encryption key pair')
    keys_parser.add_argument('--output', '-o', default='sonic_vault_keys',
                           help='Output base name for key files')
    keys_parser.add_argument('--password', '-p', 
                           help='Password to protect private key')
    
    # Info command
    subparsers.add_parser('info', help='Show system information')
    
    # Themes command
    subparsers.add_parser('themes', help='List available audio themes')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        vault = SonicVault()
        
        if args.command == 'encode':
            encode_message(vault, args)
        elif args.command == 'decode':
            decode_message(vault, args)
        elif args.command == 'generate-keys':
            generate_keys(vault, args)
        elif args.command == 'info':
            show_info(vault)
        elif args.command == 'themes':
            show_themes(vault)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def encode_message(vault, args):
    """Encode a message into audio."""
    print("🔐 SonicVault - Encoding Secure Message")
    print("=" * 50)
    
    # Validate password strength
    is_valid, msg = vault.validate_password(args.password)
    if not is_valid:
        print(f"❌ Password too weak: {msg}")
        print("💡 Please use a stronger password (min 8 chars with mix of characters)")
        return
    
    # Handle private key password if signing
    private_key_password = None
    if args.sign and args.private_key:
        private_key_password = input("🔑 Enter private key password: ")
    
    # Perform encoding
    print("🔄 Processing...")
    result = vault.encode_message(
        message=args.message,
        password=args.password,
        output_file=args.output,
        theme=args.theme,
        sign=args.sign,
        private_key_path=args.private_key
    )
    
    print(f"✅ Message encoded successfully!")
    print(f"📁 Output file: {result['output_file']}")
    print(f"⏱️  Audio duration: {result['audio_duration_seconds']:.2f} seconds")
    print(f"🎵 Sound theme: {result['theme']}")
    print(f"📝 Signed: {'Yes' if result['signed'] else 'No'}")
    
    if result['signed'] and result['private_key_path']:
        public_key = result['private_key_path'].replace('_private.pem', '_public.pem')
        print(f"🔑 Private key: {result['private_key_path']}")
        print(f"🔑 Public key: {public_key}")

def decode_message(vault, args):
    """Decode a message from audio."""
    print("🔐 SonicVault - Decoding Secure Message") 
    print("=" * 50)
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"❌ Input file not found: {args.input}")
        return
    
    # Perform decoding
    result = vault.decode_message(
        audio_file=args.input,
        password=args.password,
        public_key_path=args.public_key
    )
    
    if result['success']:
        print("✅ Message decoded successfully!")
        print(f"💬 Message: {result['message']}")
        
        if result['signature_valid'] is not None:
            status = "✅ Valid" if result['signature_valid'] else "❌ Invalid"
            print(f"📝 Signature: {status}")
    else:
        print("❌ Failed to decode message")
        print(f"💬 Error: {result['message']}")

def generate_keys(vault, args):
    """Generate encryption key pair."""
    print("🔑 SonicVault - Generating Key Pair")
    print("=" * 50)
    
    private_key = f"{args.output}_private.pem"
    public_key = f"{args.output}_public.pem"
    
    result = vault.generate_keypair(
        private_key_path=private_key,
        public_key_path=public_key,
        password=args.password
    )
    
    print("✅ Key pair generated successfully!")
    print(f"🔐 Private key: {result['private_key_path']}")
    print(f"🔓 Public key: {result['public_key_path']}")
    print(f"📏 Key size: {result['key_size']} bits")
    
    if args.password:
        print("🔒 Private key is password-protected")
    else:
        print("⚠️  Private key is NOT password-protected")

def show_info(vault):
    """Show system information."""
    print("🔐 SonicVault - System Information")
    print("=" * 50)
    
    info = vault.get_system_info()
    
    print(f"🔄 Version: {info['version']}")
    print("\n🔧 Components:")
    print(f"  • Encryption: {info['components']['aes_encryption']}")
    print(f"  • Signatures: {info['components']['dsa_signatures']}")
    print(f"  • Audio Themes: {len(info['components']['audio_themes'])} available")
    print(f"  • Morse Support: {info['components']['morse_support']} characters")
    
    print("\n🎵 Available Audio Themes:")
    for theme in info['components']['audio_themes']:
        print(f"  • {theme}")

def show_themes(vault):
    """List available audio themes."""
    print("🎵 SonicVault - Available Audio Themes")
    print("=" * 50)
    
    themes = vault.get_audio_themes()
    
    for theme in themes:
        print(f"• {theme}")

def confirm(prompt: str) -> bool:
    """Ask for user confirmation."""
    response = input(f"{prompt} (y/N): ").strip().lower()
    return response in ['y', 'yes']

if __name__ == '__main__':
    main()
