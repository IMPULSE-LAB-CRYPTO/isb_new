from cryptography.hazmat.primitives.asymmetric import rsa  # Для генерации ключей RSA
from cryptography.hazmat.primitives import serialization, hashes  # Для сериализации ключей в PEM-формат Хэш-ф OAEP
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding  # Схемы дополнения для RSA (OAEP/PKCS)
from cryptography.hazmat.backends import default_backend  # Бэкенд OpenSSL/TSL

class RSACipher:
    def __init__(self, key_size=2048):
        """
        Конструктор класса
        :param key_size: длина ключа
        """
        self.key_size = key_size

    def generate_keys(self):
        """
        Генерация пар ключей RSA
        :return: пара public и private key
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key

    def serialize_private_key(self, private_key, file_path):
        """
        Сериализация для приватного ключа в Pem файл
        :param private_key: Приватный ключ
        :param file_path: Путь сохранения
        """
        with open(file_path, 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

    def serialize_public_key(self, public_key, file_path):
        """
        Сериализация для ппубличного ключа в Pem файл
        :param public_key: Публичный ключ
        :param file_path: Путь сохранения
        """
        with open(file_path, 'wb') as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    def load_private_key(self, file_path):
        """
        Загрузка приватного ключа из файла Pem
        :param file_path: путь к файлу
        :return: Сериализация приватного ключа
        """
        with open(file_path, 'rb') as f:
            return serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )

    def load_public_key(self, file_path):
        """
        Загрузка публичного ключа тз файла Pem
        :param file_path: путь к файлу
        :return: Сериализация публичного ключа
        """
        with open(file_path, 'rb') as f:
            return serialization.load_pem_public_key(
                f.read(),
                backend=default_backend()
            )

    def encrypt(self, plaintext, public_key):
        """
        Шифрование данных с RSA публичным ключом
        :param plaintext: Передаваемый текст
        :param public_key: Публичный ключ
        :return: Зашифрованные данные
        """
        return public_key.encrypt(
            plaintext,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def decrypt(self, ciphertext, private_key):
        """
        Расшифрование данных с RSA приватным ключом
        :param ciphertext: Зашифрованный текст
        :param private_key: Приватный ключ
        :return: Расшифрованные данные
        """
        return private_key.decrypt(
            ciphertext,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )