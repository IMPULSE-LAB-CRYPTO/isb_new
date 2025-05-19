import os  # Для генерации криптографически безопасных случайных байтов (os.urandom)
from cryptography.hazmat.primitives import padding  # Реализация схем дополнения дл выравнивания данных под размер блока
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  # Классы для блочных шифров и режимов
from cryptography.hazmat.backends import default_backend  # Базовая криптографическая реализация


class BlowfishCipher:
    def __init__(self, key_length=448):
        if key_length < 32 or key_length > 448 or key_length % 8 != 0:
            raise ValueError("Blowfish Ключ должен быть от 32 до 448, делиться на 8")
        self.key_length = key_length
        self.block_size = 64  # Размер блока Blowfish — 64 бита (8 байт)

    def generate_key(self):
        """Генерация рандомного ключа Blowfish"""
        return os.urandom(self.key_length // 8)  # Байтовая строка

    def encrypt(self, plaintext, key):
        """Шифрование данных Blowfish в CBC режиме (Уникальность шифротекста при повтор данных. Пример - пингвин)"""
        init_vec = os.urandom(8)  # IV size = block size (8 bytes)

        # Apply padding
        padder = padding.PKCS7(self.block_size).padder()
        padded_data = padder.update(plaintext) + padder.finalize()

        # Encrypt
        cipher = Cipher(
            algorithms.Blowfish(key),
            modes.CBC(init_vec),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return init_vec + ciphertext  # Prepend IV to ciphertext