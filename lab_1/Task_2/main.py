from constants import *


def write_to_file(filename, content):
    """
    Записывает содержимое в файл
    :param filename: имя файла
    :param content: содержимое для записи
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


def read_file(filename):
    """
    Читает данные из файл
    :param filename: имя файла
    """
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def calculate_freq_index(text):
    """
    Вычисляет индекс частот появления букв в нашем тексте
    :param text: исходный текст
    :return: словарь, где ключ — символ, значение — процент его встречаемости
    """
    char_count = {}  # Словарь
    text_len = len(text)

    # Подсчет кол-ва символов в тексте
    for char in text:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
            
    char_percentages = {}
    for char, count in char_count.items():
        char_percentages[char] = (count / text_len)

    return char_percentages
    

def create_crypt_key(reduction_dict, decrypt_key):
    """
    Создает словарь CRYPT_KEY на основе REDUCTION_TO_SINGLE_ALPHABET и DECRYPT_KEY_FROM_SINGLE_ALPHABET
    :param reduction_dict: словарь REDUCTION_TO_SINGLE_ALPHABET
    :param decrypt_key: словарь DECRYPT_KEY_FROM_SINGLE_ALPHABET
    :return: словарь CRYPT_KEY
    """
    # Создаем обратный словарь для REDUCTION_TO_SINGLE_ALPHABET
    reverse_reduction_dict = {val: key for key, val in reduction_dict.items()}

    crypt_key = {}
    for encrypted_char, decrypted_char in decrypt_key.items():
        # Находим зашифрованный символ через обратный словарь
        if encrypted_char in reverse_reduction_dict:
            original_encrypted_char = reverse_reduction_dict[encrypted_char]
            
            crypt_key[original_encrypted_char] = decrypted_char

    return crypt_key


def main():
    try:
        # Чтение файла
        original_text = read_file(PATH_TO_ENCRYPTED_TEXT)

        # Зашифрованный текст
        print("\nЗашифрованный текст:\n")
        print(original_text)

        # Свод к единому алфавиту
        text = original_text
        for char in text:
            if char in REDUCTION_TO_SINGLE_ALPHABET:
                text = text.replace(char, REDUCTION_TO_SINGLE_ALPHABET[char])

        print("__________________________________________\n\nСвод к единому алфавиту:\n")
        print(text)

        # Расчет частот
        percent_dict = calculate_freq_index(text)

        # Сортировка частот
        print("\n_________________________________________\n\nИндекс частот зашифрованного текста:\n")
        sorted_dict = {}
        for key in sorted(percent_dict, key=percent_dict.get, reverse=True):
            sorted_dict[key] = percent_dict[key]
        print(sorted_dict)

        # Дешифровка
        print("\n___________________________________________\n\nДешифрованный текст:\n")
        for char in text:
            if char in DECRYPT_KEY_FROM_SINGLE_ALPHABET:
                text = text.replace(char, DECRYPT_KEY_FROM_SINGLE_ALPHABET[char])
        print(text)

        # Создание ключа
        crypt_key = create_crypt_key(REDUCTION_TO_SINGLE_ALPHABET, DECRYPT_KEY_FROM_SINGLE_ALPHABET)
        print("\nКлюч шифрования:\n")
        print(crypt_key)

        # Запись результатов
        write_to_file(PATH_TO_WRITE_DECRYPTED_TEXT_FILE, text)
        write_to_file(PATH_TO_WRITE_KEY, str(crypt_key))
        print("\nРезультаты успешно записаны в файлы")

    except FileNotFoundError:
        print("Ошибка: файл зашифрованного текста не найден")
    except UnicodeDecodeError:
        print("Ошибка: проблема с кодировкой файла")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()