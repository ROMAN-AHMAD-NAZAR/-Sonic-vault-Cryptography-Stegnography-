"""Setup configuration for SonicVault."""
from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="sonic-vault",
    version="1.0.0",
    author="SonicVault Team",
    description="Secure Audio Steganography - Hide encrypted messages in ambient audio soundscapes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sonic_vault",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/sonic_vault/issues",
        "Documentation": "https://github.com/yourusername/sonic_vault/docs",
        "Source Code": "https://github.com/yourusername/sonic_vault",
    },
    packages=find_packages(where="src", include=["*"]),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Security :: Cryptography",
        "Topic :: Multimedia :: Sound/Audio",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "cryptography>=41.0.0",
        "pydub>=0.25.1",
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "librosa>=0.10.0",
        "soundfile>=0.12.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sonic-vault=cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
