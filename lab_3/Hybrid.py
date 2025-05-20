from crypto.Sym_Blowfish import BlowfishCipher
from crypto.Asym_RSA import RSACipher


class HybridCryptoSystem:
    def __init__(self, symmetric_key_length=448):
        """
        Конструктор класса (инициализирует оба шифра)
        :param symmetric_key_length: Длина ключа
        """
        self.blowfish = BlowfishCipher(symmetric_key_length)
        self.rsa = RSACipher()

    def generate_keys(self):
        """
        Генерация всех необходимых ключей
        :return: симметричный ключ для Blowfish, пара ключей RSA
        """
        symmetric_key = self.blowfish.generate_key()
        private_key, public_key = self.rsa.generate_keys()
        return symmetric_key, private_key, public_key

    def encrypt_symmetric_key(self, symmetric_key, public_key):
        """
        Зашифровка симметричного ключа через RSA
        :param symmetric_key: Симметричный ключ
        :param public_key: Публичный ключ
        :return: Зашифрованный ключ Blowfish
        """
        return self.rsa.encrypt(symmetric_key, public_key)

    def decrypt_symmetric_key(self, encrypted_key, private_key):
        """
        Расшифровка симметричного ключа через RSA
        :param encrypted_key: Зашифрованный симметричный ключ
        :param private_key: Приватный ключ
        :return: Расшифрованный ключ Blowfish
        """
        return self.rsa.decrypt(encrypted_key, private_key)

    def encrypt_file(self, plaintext, symmetric_key):
        """
        Шифрование файлов посредством Blowfish
        :param plaintext: Передаваемый текст
        :param symmetric_key: Симметричный ключ
        :return: Зашифрованный файл
        """
        return self.blowfish.encrypt(plaintext, symmetric_key)

    def decrypt_file(self, ciphertext, symmetric_key):
        """
        Расшифровка файлов посредством Blowfish
        :param ciphertext: Зашифрованный текст
        :param symmetric_key: Симметричный ключ
        :return: Расшифрованный файл
        """
        return self.blowfish.decrypt(ciphertext, symmetric_key)