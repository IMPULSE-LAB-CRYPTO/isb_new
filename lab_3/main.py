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
    """Проверка на существования директории """
    if not os.path.exists('texts'):
        os.makedirs('texts')


def read_file(file_path):
    """Чтение данных из файла (бинарный режим)"""
    with open(file_path, 'rb') as f:
        return f.read()


def write_file(file_path, data):
    """Запись данных в файл (бинарный режим)"""
    with open(file_path, 'wb') as f:
        f.write(data)


def main():
    args = parsing()
    try:
        # Загрузка сгенерированной последовательности
        print("")

    except FileNotFoundError:
        print("Ошибка: файл зашифрованного текста не найден")
    except UnicodeDecodeError:
        print("Ошибка: проблема с кодировкой файла")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()