# 🔐 SonicVault - Secure Audio Steganography

A comprehensive security system that combines cryptography and audio steganography for secure covert communication. Hide encrypted messages in ambient audio soundscapes!

## ✨ Features

- **🔐 AES-256 Encryption** - Military-grade message encryption
- **📝 DSA Digital Signatures** - Authentication and integrity verification  
- **🎵 Multiple Audio Themes** - Hide messages in different sound types
- **⚡ Morse Code Encoding** - Robust timing-based communication
- **🔑 Key Management** - Secure key generation and storage
- **📁 File Export** - Standard WAV audio format

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd sonic_vault

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Encode a secret message
python cli.py encode "Meet at midnight" secret.wav --password MyPass123 --theme rain

# Decode the message
python cli.py decode secret.wav --password MyPass123

# Generate encryption keys
python cli.py generate-keys --output my_keys --password KeyPassword123

# Show system information
python cli.py info
```

## 📖 Commands

### Encode Messages
```bash
python cli.py encode "Your secret message" output.wav \
  --password YourPassword \
  --theme rain \
  --sign \
  --private-key my_private.pem
```

### Decode Messages  
```bash
python cli.py decode input.wav \
  --password YourPassword \
  --public-key my_public.pem
```

### Key Management
```bash
# Generate new key pair
python cli.py generate-keys --output my_keys --password KeyPassword

# List audio themes
python cli.py themes

# System information
python cli.py info
```

## 🎵 Audio Themes

- **sine** - Clean sine wave tones
- **rain** - Raindrop-like sounds
- **birds** - Bird chirp sounds  
- **synth** - Electronic synth tones
- **digital** - Digital beep sounds

## 🔧 Technical Details

### Security Features
- **AES-256-CBC** encryption with PBKDF2 key derivation
- **DSA-2048** digital signatures with SHA-256
- **Random salts and IVs** for each encryption
- **Password-protected private keys**

### Audio Encoding
- **Morse code** conversion with timing patterns
- **44.1 kHz WAV** format output
- **Configurable timing** for dots and dashes
- **Multiple sound generation** algorithms

## 🗂️ Project Structure

```
sonic_vault/
├── src/
│   ├── core/           # Main application logic
│   ├── crypto/         # Encryption and signatures
│   ├── audio/          # Audio processing
│   └── utils/          # Helper functions
├── tests/              # Comprehensive test suite
├── docs/               # Documentation
└── examples/           # Usage examples
```

## 🧪 Testing

Run the complete test suite:

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test categories
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v
```

## 📊 System Requirements

- **Python 3.8+**
- **Dependencies**: cryptography, pydub, numpy, librosa
- **Platform**: Windows, macOS, Linux

## 🔒 Security Notice

This is an educational project. For production use, consult security professionals and consider additional security measures like:
- Secure key storage
- Network transmission security
- Side-channel attack protection
- Regular security audits

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

[Add your license here]

---

**SonicVault** - Because sometimes the best place to hide is in plain hearing! 👂
