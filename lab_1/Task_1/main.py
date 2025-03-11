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


def main():
    alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя "

    with open('original_text.txt', 'r', encoding='utf-8') as file:
        original_text = file.read()
    with open('key.txt', 'r', encoding='utf-8') as file:
        key = file.read()


    shifr_text = shifr(original_text, key, alphabet)
    print("Зашифрованный текст: ")
    print(shifr_text)

    save_to_file("shifr_text.txt", shifr_text)
    print("\nДанные сохранены в файлы: original_text.txt, encrypted_text.txt, key.txt")


if __name__ == "__main__":
    main()

