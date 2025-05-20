import os
import argparse
from Hybrid import HybridCryptoSystem
from Config_Manager import ConfigManager


def parsing() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки
    """
    parser = argparse.ArgumentParser(description='Гибридная криптосистема RSA + Blowfish')
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-gen', '--generation', action='store_true', help='Запускает режим генерации ключей')
    group.add_argument('-enc', '--encryption', action='store_true', help='Запускает режим шифрования')
    group.add_argument('-dec', '--decryption', action='store_true', help='Запускает режим дешифрования')

    # Общие параметры
    parser.add_argument('--key-length', type=int, default=448,
                        help='Длина ключа Blowfish (32-448 бит, шаг 8) - только для генерации')

    # parser.add_argument('--input', default='texts/original.txt', help='Входной файл (для шифрования/дешифрования)')
    # parser.add_argument('--output', default=None, help='Выходной файл (для шифрования/дешифрования)')

    args = parser.parse_args()
    return args


def ensure_texts_dir():
    """Проверка на существования директории """
    if not os.path.exists('texts'):
        os.makedirs('texts')
    if not os.path.exists('keys'):
        os.makedirs('keys')


def read_file(file_path):
    """Чтение данных из файла (бинарный режим)"""
    with open(file_path, 'rb') as f:
        return f.read()


def write_file(file_path, data):
    """Запись данных в файл (бинарный режим)"""
    with open(file_path, 'wb') as f:
        f.write(data)


def main():
    config = ConfigManager()

    args = parsing()
    ensure_texts_dir()
    crypto = HybridCryptoSystem()
    try:
        if args.generation:
            # Режим генерации ключей
            print("Генерация ключей...")
            crypto = HybridCryptoSystem(args.key_length)
            symmetric_key, private_key, public_key = crypto.generate_keys()

            # Сохранение ключей
            crypto.rsa.serialize_private_key(private_key, config.get_setting('private_key'))
            crypto.rsa.serialize_public_key(public_key, config.get_setting('public_key'))

            # Шифрование и сохранение симметричных ключей
            encrypted_key = crypto.encrypt_symmetric_key(symmetric_key, public_key)
            write_file(config.get_setting('symmetric_key'), encrypted_key)

            print("Ключи успешно сгенерированы (в папку keys):")
            print(f"- Симметричный ключ (зашифрованный): sym_key.enc")
            print(f"- Открытый ключ RSA: public.pem")
            print(f"- Закрытый ключ RSA: private.pem")
            print(f"Длина ключа Blowfish: {args.key_length} бит")

        elif args.encryption:
            # Режим шифрования
            print("Шифрование файла...")

            # Загружаем ключи
            private_key = crypto.rsa.load_private_key(config.get_setting('private_key'))

            encrypted_key = read_file(config.get_setting('symmetric_key'))

            # Расшифровка симметричных ключей
            symmetric_key = crypto.decrypt_symmetric_key(encrypted_key, private_key)

            # Чтение и шифрование файла
            plaintext = read_file(config.get_setting('initial_file'))
            ciphertext = crypto.encrypt_file(plaintext, symmetric_key)
            write_file(config.get_setting('encrypted_file'), ciphertext)

            print(f"Файл успешно зашифрован: {config.get_setting('encrypted_file')}")

        elif args.decryption:
            # Режим расшифровки
            print("Дешифрование файла...")

            # Загрузка ключей
            private_key = crypto.rsa.load_private_key(config.get_setting('private_key'))
            encrypted_key = read_file(config.get_setting('symmetric_key'))

            # Расшифровка симметричного ключа
            symmetric_key = crypto.decrypt_symmetric_key(encrypted_key, private_key)

            # Чтение и расшифровка файла
            ciphertext = read_file(config.get_setting('encrypted_file'))
            plaintext = crypto.decrypt_file(ciphertext, symmetric_key)
            write_file(config.get_setting('decrypted_file'), plaintext)

            print(f"Файл успешно расшифрован: {config.get_setting('decrypted_file')}")

    except FileNotFoundError:
        print("Ошибка: файл с текстом не найден")
    except UnicodeDecodeError:
        print("Ошибка: проблема с кодировкой файла")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        exit(1)


if __name__ == "__main__":
    main()