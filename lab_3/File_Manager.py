import os


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