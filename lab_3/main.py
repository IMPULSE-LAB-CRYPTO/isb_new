import os
import argparse

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
    parser.add_argument('--key-length', type=int, default=448, help='Длина ключа Blowfish (32-448 бит, шаг 8) - только для генерации')
    parser.add_argument('--input', default='texts/original.txt', help='Входной файл (для шифрования/дешифрования)')
    parser.add_argument('--output', default=None, help='Выходной файл (для шифрования/дешифрования)')

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
        if args.generation:
            # Key generation mode
            print("Генерация ключей...")

            # Save keys (Здесь будет сохранение)

        elif args.encryption:
            # Encryption mode
            print("Шифрование файла...")

        elif args.decryption:
            # Decryption mode
            print("Дешифрование файла...")


    except FileNotFoundError:
        print("Ошибка: файл зашифрованного текста не найден")
    except UnicodeDecodeError:
        print("Ошибка: проблема с кодировкой файла")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        exit(1)

if __name__ == "__main__":
    main()