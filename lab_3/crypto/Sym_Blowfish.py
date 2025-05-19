import os  # Для генерации криптографически безопасных случайных байтов (os.urandom)
from cryptography.hazmat.primitives import padding  # Реализация схем дополнения дл выравнивания данных под размер блока
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  # Классы для блочных шифров и режимов
from cryptography.hazmat.backends import default_backend  # Базовая криптографическая реализация


class BlowfishCipher:
    def __init__(self, key_length=448):
        """
        Конструктор класса
        :param key_length: длина ключа (условный параметр - 448)
        """
        if key_length < 32 or key_length > 448 or key_length % 8 != 0:
            raise ValueError("Blowfish Ключ должен быть от 32 до 448, делиться на 8")
        self.key_length = key_length
        self.block_size = 64  # Размер блока Blowfish — 64 бита (8 байт)

    def generate_key(self):
        """
        Генерация рандомного ключа Blowfish
        :return: Ключ в виде байтовой строки
        """
        return os.urandom(self.key_length // 8)

    def encrypt(self, plaintext, key):
        """
        Шифрование данных Blowfish в CBC режиме (Уникальность шифротекста при повтор данных. Пример - пингвин)
        :param plaintext: Передаваемый текст
        :param key: Ключ шифрования
        :return: init_vec + ciphertext (уникальные байты + зашифрованные данные)
        """
        init_vec = os.urandom(8)  # IV размер = размер блока (8 байт)

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

        return init_vec + ciphertext  # Добавление IV к ciphertext

    def decrypt(self, ciphertext, key):
        """
        Расшифрока данных Blowfish в CBC режиме
        :param ciphertext: Зашифрованный текст
        :param key: Ключ шифрования
        :return: Исходные данные без IV и дополнения.
        """

        # Извлечение IV (первые 8 байт)
        init_vec = ciphertext[:8]
        ciphertext = ciphertext[8:]

        # Расшифровка
        cipher = Cipher(
            algorithms.Blowfish(key),
            modes.CBC(init_vec),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

        # Удаление padding
        unpadder = padding.PKCS7(self.block_size).unpadder()
        decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

        return decrypted