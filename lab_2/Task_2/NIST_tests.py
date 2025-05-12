from constants import *

import math
import re
from scipy.special import gammainc

def read_file(filename):
    """
    Читает данные из файла, обрезая пробельные символы
    :param filename: имя файла
    """
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().strip()


def write_to_file(filename, content_1, content_2, content_3):
    """
    Записывает содержимое в файл в формате:
    :param filename: имя файла для записи (включая путь при необходимости)
    :param content_1: результат частотного теста
    :param content_2: результат теста на серии
    :param content_3: результат теста на длинные серии
    """
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"Значение частотного теста P-value: {content_1}")

        file.write(f"\nЗначение теста на одинаковые подряд идущие биты P-value: {content_2}")

        file.write(f"\nЗначение теста на самую длинную последовательность: {content_3}")


def frequency_test(sequence):
    """
    Проверяет, что количество нулей и единиц в последовательности примерно одинаково
    :param sequence: Передаваемая последовательность (бит)
    :return: P-значение (если P->0 значит seq предсказуема, P->1 - seq случайна)
    """
    n = len(sequence)
    ones = sequence.count('1')
    zeros = sequence.count('0')
    sum = ones - zeros
    S_n = abs(sum) / (n ** 0.5)
    p_value = math.erfc(S_n / (2 ** 0.5))
    return p_value


def runs_test(sequence):
    """
    Проверяет, что количество последовательностей одинаковых битов соответствует ожидаемому
    :param sequence: Передаваемая последовательность (бит)
    :return: P-значение
    """
    n = len(sequence)
    ones = sequence.count('1')

    prop = ones / n #Доля единиц в seq
    tau = 2 / (n ** 0.5)
    if abs(prop - 0.5) >= tau:
        return 0.0

    runs = 0 #Знакоперемены
    for i in range(0, n-1):
        if sequence[i] != sequence[i + 1]:
            runs += 1

    p_value = math.erfc(abs(runs - 2 * n * prop * (1 - prop)) /
                        (2 * (2 * n)**0.5 * prop * (1 - prop)))
    return p_value


def longest_run_of_ones_test(sequence, block_size=8):
    """
    Тест на самую длинную последовательность единиц в блоке
    :param sequence: Передаваемая последовательность (бит)
    :param block_size: Длина последовательности - 128, (длина блока - 8)
    :return:p_value
    """
    n = len(sequence)
    num_blocks = n // block_size
    if num_blocks == 0:
        return 0.0

    # Разделение последовательности на блоки
    blocks = []
    for i in range(num_blocks):
        start = i * block_size
        end = (i + 1) * block_size
        block = sequence[start:end]
        blocks.append(block)

    # Поиск максимальной длины последовательности единиц в каждом блоке
    max_runs = []
    for block in blocks:
        runs = re.findall('1+', block) #регулярное выражение: одна и более единица
        if runs:
            max_run = max(len(run) for run in runs)
        else:
            max_run = 0
        max_runs.append(max_run)


    # Ожидаемые значения для block_size = 128
    expected_pi = [0.2148, 0.3672, 0.2305, 0.1875]
    if block_size == 8:
        V = [0, 0, 0, 0]
        for run in max_runs:
            if run <= 1:
                V[0] += 1
            elif run == 2:
                V[1] += 1
            elif run == 3:
                V[2] += 1
            else:
                V[3] += 1

        chi_square = sum((V[i] - num_blocks * expected_pi[i]) ** 2 / (num_blocks * expected_pi[i]) for i in range(4))
        p_value = gammainc(1.5, chi_square/2)
        return p_value

    else:
        return 0.0


def main():
    try:
        # Загрузка сгенерированной последовательности
        sequence_cpp = read_file(PATH_TO_CPP_SEQ)

        sequence_java = read_file(PATH_TO_JAVA_SEQ)

        # Применение тестов
        p_value_freq_cpp = frequency_test(sequence_cpp)
        p_value_runs_cpp = runs_test(sequence_cpp)
        p_value_longest_run_cpp = longest_run_of_ones_test(sequence_cpp)

        p_value_freq_java = frequency_test(sequence_java)
        p_value_runs_java = runs_test(sequence_java)
        p_value_longest_run_java = longest_run_of_ones_test(sequence_java)

        # Вывод результатов
        print("C++ Sequence:")
        print(f"Frequency Test p-value: {p_value_freq_cpp}")
        print(f"Runs Test p-value: {p_value_runs_cpp}")
        print(f"Longest Run of Ones Test p-value: {p_value_longest_run_cpp}")
        #Проверил на калькуляторе:
        #Regularized upper incomplete gamma function: 0.63205382


        print("\nJava Sequence:")
        print(f"Frequency Test p-value: {p_value_freq_java}")
        print(f"Runs Test p-value: {p_value_runs_java}")
        print(f"Longest Run of Ones Test p-value: {p_value_longest_run_java}")
        #Проверил на калькуляторе:
        #Regularized upper incomplete gamma function: 0.63205382

        #Запись в текстовый файл результаты
        write_to_file(PATH_TO_NIST_RES_CPP, p_value_freq_cpp, p_value_runs_cpp, p_value_longest_run_cpp)
        write_to_file(PATH_TO_NIST_RES_JAVA, p_value_freq_java, p_value_runs_java, p_value_longest_run_java)

    except FileNotFoundError:
        print("Ошибка: файл зашифрованного текста не найден")
    except UnicodeDecodeError:
        print("Ошибка: проблема с кодировкой файла")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()