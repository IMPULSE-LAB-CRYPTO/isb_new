import os
import json


class ConfigManager:
    _instance = None

    def __new__(cls):
        """
        Создание нового экземпляра класса
        """
        if cls._instance is None: # Создаем новый экз класса и вызываем инициализацию
            cls._instance = super().__new__(cls)
            cls._instance.__init_config()
        return cls._instance

    def __init_config(self):
        """
        Инициализация конфига
        :return: Установка пути к файлу конфигурации
        """
        self.config_path = 'settings.json'
        self.default_config = {
            'initial_file': 'texts/original.txt',
            'encrypted_file': 'texts/encrypted.bin',
            'decrypted_file': 'texts/decrypted.txt',
            'symmetric_key': 'keys/sym_key.enc',
            'public_key': 'keys/public.pem',
            'private_key': 'keys/private.pem'
        }
        self.__ensure_config_exists()

    def __ensure_config_exists(self):
        """
        Создание файла настроек, если его нет
        :return: Обновленный конфиг
        """
        if not os.path.exists(self.config_path):
            self._create_directories()
            self.save_config(self.default_config)
        else:
            # Проверяем, что все необходимые ключи присутствуют в файле
            with open(self.config_path, 'r') as f:
                existing_config = json.load(f)
                for key in self.default_config:
                    if key not in existing_config:
                        existing_config[key] = self.default_config[key]
                self.save_config(existing_config)

    def __create_directories(self):
        """
        Создание необходимых директорий
        :return: Обновленные директории
        """
        os.makedirs('texts', exist_ok=True)
        os.makedirs('keys', exist_ok=True)

    def _load_config(self):
        """
        Возвращение текущих настроек
        :return: Текущие настройки
        """
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def save_config(self, config):
        """
        Сохранение настроек в файл
        :param config: Подаваемая конфигурация
        :return: Сохранение конфига в файл
        """
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=4)

    def get_setting(self, key):
        """
        Получение конкретных настроек
        :param key: Входной параметр
        :return: Конкретный параметр
        """
        config = self._load_config()
        return config.get(key)