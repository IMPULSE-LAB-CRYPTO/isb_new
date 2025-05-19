import os

class BlowfishCipher:
    def __init__(self, key_length=448):
        if key_length < 32 or key_length > 448:
            raise ValueError("Blowfish key length must be between 32 and 448 bits")
        self.key_length = key_length
        self.block_size = 64  # Blowfish block size in bits (8 bytes)
