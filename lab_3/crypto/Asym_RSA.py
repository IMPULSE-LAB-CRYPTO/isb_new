from cryptography.hazmat.primitives.asymmetric import rsa  # Для генерации ключей RSA


class RSACipher:
    def __init__(self, key_size=2048):
        self.key_size = key_size

    def generate_keys(self):
        """Generate RSA key pair"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key
