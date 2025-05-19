import os
import argparse

def parsing() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки
    """
    parser = argparse.ArgumentParser(description='Гибридная криптосистема RSA + Blowfish')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Key generation mode
    gen_parser = subparsers.add_parser('gen', help='Генерация ключей')
    gen_parser.add_argument('--key-length', type=int, default=448, help='Длина ключа Blowfish (32-448 бит, шаг 8)')

    # Encryption mode
    enc_parser = subparsers.add_parser('enc', help='Шифрование файла')
    enc_parser.add_argument('--input', default='texts/original.txt', help='Файл для шифрования')
    enc_parser.add_argument('--output', default='texts/encrypted.bin', help='Файл для зашифрованных данных')

    # Decryption mode
    dec_parser = subparsers.add_parser('dec', help='Дешифрование файла')
    dec_parser.add_argument('--input', default='texts/encrypted.bin', help='Файл для дешифрования')
    dec_parser.add_argument('--output', default='texts/decrypted.txt', help='Файл для расшифрованных данных')

    args = parser.parse_args()
    return args

def ensure_texts_dir():
    """Ensure texts directory exists"""
    if not os.path.exists('texts'):
        os.makedirs('texts')

