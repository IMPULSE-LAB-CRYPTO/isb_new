import os


class FileManager:
    """
    Класс для управления файловыми операциями: создание директорий, чтение и запись файлов.
    """
    def __init__(self, texts_dir='texts', keys_dir='keys'):
        """
        Инициализация FileManager
        :param texts_dir: Название директории для текстов
        :param keys_dir: Название директории для ключей
        """
        self._texts_dir = texts_dir
        self._keys_dir = keys_dir
        self.ensure_dirs_exist()

    def ensure_dirs_exist(self):
        """
        Приватный метод для проверки и создания необходимых директорий, если они не существуют.
        :return: Создание необходимых директорий
        """
        if not os.path.exists(self._texts_dir):
            os.makedirs(self._texts_dir)
        if not os.path.exists(self._keys_dir):
            os.makedirs(self._keys_dir)

    def read_file(self, file_path):
        """
        Чтение данных из файла в бинарном режиме
        :param file_path: Путь к файлу для чтения
        :return: Содержимое файла в бинарном виде
        """
        with open(file_path, 'rb') as f:
            return f.read()

    def write_file(self, file_path, data):
        """
        :param file_path: Путь к файлу для записи
        :param data: Данные для записи в файл
        :return: Записанные данные в файл
        """
        with open(file_path, 'wb') as f:
            f.write(data)

    @property
    def texts_dir(self):
        """
        Получение пути к директории с текстами (только для чтения)
        :return: Путь
        """
        return self._texts_dir

    @property
    def keys_dir(self):
        """
        Получение пути к директории с ключами (только для чтения)
        :return: Путь
        """
        return self._keys_dir