from constants import *


def shifr(text, key, alphabet):
    """
    Функция кодирования текста при помощи метода Вижинера
    :param text: шифруемый текст
    :param key: ключ шифрования
    :param alphabet: алфавит шифрования
    :return: зашифрованный текст
    """
    key = key.lower()
    key_length = len(key)
    shifr_text = ''
    alphabet_size = len(alphabet)

    for i in range (len(text)):
        char = text[i]
        if char.lower() in alphabet:
            key_char = key[i % key_length].lower()
            shift = alphabet.find(key_char)

            char_index = alphabet.find(char.lower())

            new_index = (char_index + shift) % alphabet_size

            if char.isupper():
                shifr_text += alphabet[new_index].upper()
            else:
                shifr_text += alphabet[new_index]
        else:
            shifr_text += char

    return shifr_text

def save_to_file(filename, data):
    """
    Сохраняет данные в файл
    :param filename: имя файла
    :param data: данные для сохранения
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(data)


def read_file(filename):
    """
    Читает данные из файл
    :param filename: имя файла
    """
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def main():
    original_text = read_file(PATH_TO_TEXT_FILE)
    key = read_file(PATH_TO_KEY_FILE)

    shifr_text = shifr(original_text, key, ALPHABET)
    print("Зашифрованный текст: ")
    print(shifr_text)

    save_to_file(PATH_TO_WRITE_TEXT_FILE, shifr_text)
    print("\nДанные сохранены в файлы: shifr_text.txt")


if __name__ == "__main__":
    main()

