"""
Morse Code utilities for SonicVault.
"""

class MorseCode:
    """
    Handles conversion between text and Morse code with error resilience.
    """
    
    # International Morse code dictionary
    MORSE_CODE_DICT = {
        'A': '.-',      'B': '-...',    'C': '-.-.',    'D': '-..',     'E': '.',      
        'F': '..-.',    'G': '--.',     'H': '....',    'I': '..',      'J': '.---',
        'K': '-.-',     'L': '.-..',    'M': '--',      'N': '-.',      'O': '---',
        'P': '.--.',    'Q': '--.-',    'R': '.-.',     'S': '...',     'T': '-',
        'U': '..-',     'V': '...-',    'W': '.--',     'X': '-..-',    'Y': '-.--',
        'Z': '--..',    '0': '-----',   '1': '.----',   '2': '..---',   '3': '...--',
        '4': '....-',   '5': '.....',   '6': '-....',   '7': '--...',   '8': '---..',
        '9': '----.',   '.': '.-.-.-',  ',': '--..--',  '?': '..--..',  "'": '.----.',
        '!': '-.-.--',  '/': '-..-.',   '(': '-.--.',   ')': '-.--.-',  '&': '.-...',
        ':': '---...',  ';': '-.-.-.',  '=': '-...-',   '+': '.-.-.',   '-': '-....-',
        '_': '..--.-',  '"': '.-..-.',  '$': '...-..-', '@': '.--.-.',  '|': '...-.-',
        ' ': '/'
    }
    
    # Reverse dictionary for decoding
    REVERSE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}
    
    def _normalize_text(self, text: str) -> str:
        """
        Normalize input text by uppercasing, trimming, and collapsing whitespace.
        """
        if text is None:
            return ""
        # Strip leading/trailing whitespace and collapse internal runs to single spaces
        stripped = text.strip()
        if not stripped:
            return ""
        return ' '.join(stripped.split())

    def text_to_morse(self, text: str) -> str:
        """
        Convert text to Morse code.
        """
        normalized = self._normalize_text(text)
        if not normalized:
            return ""
        
        morse_parts = []
        for char in normalized:
            if char == ' ':
                morse_parts.append('/')
                continue
            
            lookup = char
            if lookup not in self.MORSE_CODE_DICT and char.isalpha():
                lookup = char.upper()
            
            if lookup in self.MORSE_CODE_DICT:
                morse_parts.append(self.MORSE_CODE_DICT[lookup])
            else:
                raise ValueError(f"Unsupported character for Morse code: '{char}'")
        
        return ' '.join(morse_parts)
    
    def morse_to_text(self, morse_code: str, skip_errors: bool = False) -> str:
        """
        FIXED: Convert Morse code back to text with maximum error resilience.
        
        Args:
            morse_code: Morse code string to decode
            skip_errors: If True, skip invalid characters instead of failing
        """
        if not morse_code:
            return ""
        
        text_parts = []
        normalized = morse_code.strip()
        if not normalized:
            return ""
        
        # Accept "/" as separator even without surrounding spaces
        words = [word.strip() for word in normalized.split('/') if word.strip()]
        
        for word in words:
            chars = word.split(' ')
            word_text = []
            
            for morse_char in chars:
                if not morse_char:
                    continue
                    
                morse_char = morse_char.strip()
                
                # Direct lookup
                if morse_char in self.REVERSE_DICT:
                    word_text.append(self.REVERSE_DICT[morse_char])
                else:
                    if skip_errors:
                        # Try to recover by length-based guessing
                        recovered = self._recover_morse_char(morse_char)
                        if recovered:
                            word_text.append(recovered)
                            continue
                        # Skip invalid sequences silently when skipping errors
                        continue
                    raise ValueError(f"Invalid Morse pattern: '{morse_char}'")
            
            if word_text:
                text_parts.append(''.join(word_text))
        
        result = ' '.join(text_parts)
        print(f"   📝 Morse Decoding: '{result}'")
        return result
    
    def _recover_morse_char(self, morse_char: str) -> str:
        """
        Attempt to recover corrupted Morse characters.
        """
        # Common corruptions and their likely intended characters
        recovery_map = {
            '.....': '5',
            '....': 'H',     # H is ...., not 4
            '...': 'S',
            '..': 'I',
            '.': 'E',
            '.-.': 'R',
            '-.': 'N',
            '--': 'M',
            '-': 'T',
            '.-': 'A',
        }
        
        # Try exact match first
        if morse_char in recovery_map:
            return recovery_map[morse_char]
        
        # If all else fails, return empty string to skip
        return ''

    def get_supported_characters(self) -> list:
        """
        Get list of supported characters.
        """
        return list(self.MORSE_CODE_DICT.keys())    

    def validate_text(self, text: str) -> bool:
        """
        Validate that text contains only supported characters and is non-empty.
        """
        normalized = self._normalize_text(text)
        if not normalized:
            return False
        for char in normalized:
            if char == ' ':
                continue
            lookup = char
            if lookup not in self.MORSE_CODE_DICT and char.isalpha():
                lookup = char.upper()
            if lookup not in self.MORSE_CODE_DICT:
                return False
        return True