import math

vocab_simp = list('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')# полный русский алфавит
vocab_simp_en = list('abcdefghijklmnopqrstuvwxyz')# полный английский алфавит


def gcd_explore(alphabet):
    """
    ПОИСК ВСЕВОЗМОЖНЫХ ALPHA
    :param alphabet: используемый алфавит
    :return: оценивая мощность алфавита, функция выводит все возможные вариации alpha в виде массива
    """
    vocab_simp = list(alphabet)
    m = len(vocab_simp)
    gcd = []
    for i in range(1, m + 1):
        if math.gcd(i, m) == 1:
            gcd.append(i)
    return gcd


def alpha_inverse(alpha, power):
    """
    НАХОЖДЕНИЕ ОБРАТНОГО ЭЛЕМЕНТА ALPHA
    :param alpha: значение, для которого надо найти обратный элемент
    :param power: мощность алфавита
    :return: обратный элемент
    """
    for inv in range(1, power):
        r = (inv * alpha) % power
        if r == 1:
            break
    else:
        raise ValueError('%d has no inverse mod %d' % (alpha, power))
    return inv


def create_keys(a1, a2, b1, b2, power, count_keys):
    """
    СОЗДАНИЕ КЛЮЧЕЙ ДЛЯ АФФИННОГО РЕКУРРЕНТНОГО ШИФРА
    :param a1: ALPHA1
    :param a2: ALPHA2
    :param b1: BETA1
    :param b2: BETA2
    :param power: мощность используемого алфавита
    :param count_keys: количество генерируемых ключей
    :return: два массива со значениями ALPHA в одном и BETA в другом соответственно
    """
    alpha_arr = [a1, a2]
    beta_arr = [b1, b2]
    for i in range(2, count_keys):
        alpha_arr.append(int((alpha_arr[i - 2] * alpha_arr[i - 1]) % power))
    for i in range(2, count_keys):
        beta_arr.append(int((beta_arr[i - 2] + beta_arr[i - 1]) % power))
    return alpha_arr, beta_arr


def encode_simple(text, key):
    """
    РЕАЛИЗАЦИЯ ШИФРА ПРОСТОЙ ЗАМЕНЫ: зашифрование
    :param text: открытый текст
    :param key: ключ
    :return: шифр текст
    """
    if len(set(key)) != len(vocab_simp):
        return "Длина ключа не совпадает с мощностью используемого алфавита или ключ неверно введен! Дальнейшая работа программы не возможна!"
    encode_text = ''
    vocab_simp_new = (key)
    for i in text:#цикл пропускает все пробелы, чтобы их не шифровать
        if i == ' ' or i == ',' or i == "." or i == ':' or i == ";":
            encode_text += ' '
            continue
        ind = int(vocab_simp.index(i))#индекс символа открытого текста
        encode_text += vocab_simp_new[ind]
    return encode_text

def decode_simple(encode_text, key):
    """
    РЕАЛИЗАЦИЯ ШИФРА ПРОСТОЙ ЗАМЕНЫ: расшифрование
    :param encode_text: шифр текст
    :param key: ключ
    :return: открытый текст
    """
    if len(set(key)) != len(vocab_simp):
        return "Длина ключа не совпадает с мощностью используемого алфавита или ключ неверно введен! Дальнейшая работа программы не возможна!"
    vocab_simp_new = (key)
    decode_text = ''
    for i in encode_text:#цикл пропускает все пробелы, чтобы их не шифровать
        if i == ' ' or i == ',' or i == "." or i == ':' or i == ";":
            decode_text += ' '
            continue
        ind = int(vocab_simp_new.index(i))#индекс символа шифр текста
        decode_text += vocab_simp[ind]
    return decode_text


def aff_encode(alphabet, open_text, alpha, beta):
    """
    РЕАЛИЗАЦИЯ АФФИННОГО ШИФРА: зашифрование
    :param alphabet: используемый алфавит
    :param open_text: открытый текст
    :param alpha: выбранная alpha
    :param beta: выбранная alpha
    :return: шифр текст
    """
    chipher = ''
    for i in open_text:  # цикл пропускает все пробелы, чтобы их не шифровать
        if i == ' ' or i == ',' or i == "." or i == ':' or i == ";":
            chipher += ' '
            continue
        chipher += alphabet[(alpha * alphabet.index(i) + beta) % len(alphabet)]
    return chipher


def aff_decode(alphabet, cipher_text, alpha, beta):
    """
    РЕАЛИЗАЦИЯ АФФИННОГО ШИФРА: расшифрование
    :param alphabet: используемый алфавит
    :param cipher_text: шифр текст
    :param alpha: выбранная alpha
    :param beta: выбранная beta
    :return: открытый текст
    """
    open_txt = ''
    alpha_inv = alpha_inverse(alpha, len(alphabet))
    for i in cipher_text:  # цикл пропускает все пробелы, чтобы их не шифровать
        if i == ' ' or i == ',' or i == "." or i == ':' or i == ";":
            open_txt += i
            continue
        open_txt += alphabet[(alpha_inv * (alphabet.index(i) - beta)) % len(alphabet)]
    return open_txt


def aff_rec_encode(open_text, alphabet, alpha1, alpha2, beta1, beta2):
    """
    РЕАЛИЗАЦИЯ АФФИННОГО РЕКУРРЕНТНОГО ШИФРА: зашифрование
    :param open_text: открытый текст
    :param alphabet: выбранный алфавит
    :param alpha1, alpha2, beta1, beta2: выбранные ключи шифрования
    :return: шифр текст
    """
    cipher = ''
    count_keys = 0
    count_symbol = 0
    for s in open_text:
        if s in alphabet:
            count_keys += 1
    alpha_arr, beta_arr = create_keys(alpha1, alpha2, beta1, beta2, len(alphabet), count_keys)
    for i in open_text:  # цикл пропускает все пробелы, чтобы их не шифровать
        if i == ' ' or i == ',' or i == "." or i == ':' or i == ";":
            cipher += i
            continue
        cipher += alphabet[(alpha_arr[count_symbol] * alphabet.index(i) + beta_arr[count_symbol]) % len(alphabet)]
        count_symbol += 1
    return cipher


def aff_rec_decode(cipher, alphabet, alpha1, alpha2, beta1, beta2):
    """
        РЕАЛИЗАЦИЯ АФФИННОГО РЕКУРРЕНТНОГО ШИФРА: расшифрование
        :param cipher: шифр текст
        :param alphabet: выбранный алфавит
        :param alpha1, alpha2, beta1, beta2: выбранные ключи шифрования
        :return: открытый текст
        """
    open_txt = ''
    count_keys = 0
    count_symbol = 0
    for s in cipher:
        if s in alphabet:
            count_keys += 1
    alpha_arr, beta_arr = create_keys(alpha1, alpha2, beta1, beta2, len(alphabet), count_keys)
    for i in cipher:  # цикл пропускает все пробелы, чтобы их не шифровать
        if i == ' ' or i == ',' or i == "." or i == ':' or i == ";":
            open_txt += i
            continue
        alpha_inv = alpha_inverse(alpha_arr[count_symbol], len(alphabet))
        open_txt += alphabet[(alpha_inv * (alphabet.index(i) - beta_arr[count_symbol])) % len(alphabet)]
        count_symbol += 1
    return open_txt


ch1 = int(input("Введите: '1' -- зашифровка, '2' -- расшифровка: "))
if ch1 == 1:
    ch2 = int(input("Введите: '1' -- шифр простой замены, '2' -- аффинный шифр, '3' -- аффинный рекуррентный шифр: "))

    if ch2 == 1: # шифр простой замены
        open_text = input("Введите текст для зашифровки: ")
        key = input("Введите ключ для зашифровки: ")
        print(encode_simple(open_text.lower(), key))

    elif ch2 == 2: # аффинный шифр
        language_choice = input("Выберите язык: '1' -- Ru, '2' -- En: ")
        open_text = input("Введите текст для зашифровки: ").lower()

        if language_choice == "1": #шифрование на русском
            print("Список допустимых alpha: ",gcd_explore(vocab_simp))
            alpha = int(input("Ваш выбор: "))
            print("Список допустимых beta: ", [x for x in range(len(vocab_simp))])
            beta = int(input("Ваш выбор: "))
            print("Зашифрованный текст: ", aff_encode(vocab_simp, open_text, alpha, beta))
            print("Значение alpha:", alpha, "|", "Значение beta:", beta)

        elif language_choice == "2": #шифрование на английском
            print("Список допустимых alpha: ", gcd_explore(vocab_simp_en))
            alpha = int(input("Ваш выбор: "))
            print("Список допустимых beta: ", [x for x in range(len(vocab_simp))])
            beta = int(input("Ваш выбор: "))
            print("Зашифрованный текст: ", aff_encode(vocab_simp_en, open_text, alpha, beta))
            print("Значение alpha:", alpha, "|", "Значение beta:", beta)

    elif ch2 == 3: # аффинный рекуррентный шифр
        language_choice = input("Выберите язык: '1' -- Ru, '2' -- En: ")
        open_text = input("Введите текст для зашифровки: ").lower()

        if language_choice == "1": #шифрование на русском
            print("Список допустимых alpha: ",gcd_explore(vocab_simp))
            alpha1 = int(input("Ваш выбор: "))
            alpha2 = int(input("Ваш выбор: "))
            print("Список допустимых beta: ", [x for x in range(len(vocab_simp))])
            beta1 = int(input("Ваш выбор: "))
            beta2 = int(input("Ваш выбор: "))
            print("Зашифрованный текст: ", aff_rec_encode(open_text, vocab_simp, alpha1, alpha2, beta1, beta2))
            print("Значение alpha1:", alpha1, "|", "Значение beta1:", beta1)
            print("Значение alpha2:", alpha2, "|", "Значение beta2:", beta2)

        elif language_choice == "2": #шифрование на английском
            print("Список допустимых alpha: ", gcd_explore(vocab_simp_en))
            alpha1 = int(input("Ваш выбор: "))
            alpha2 = int(input("Ваш выбор: "))
            print("Список допустимых beta: ", [x for x in range(len(vocab_simp))])
            beta1 = int(input("Ваш выбор: "))
            beta2 = int(input("Ваш выбор: "))
            print("Зашифрованный текст: ", aff_rec_encode(open_text, vocab_simp_en, alpha1, alpha2, beta1, beta2))
            print("Значение alpha1:", alpha1, "|", "Значение beta1:", beta1)
            print("Значение alpha2:", alpha2, "|", "Значение beta2:", beta2)

elif ch1 == 2:
    ch2 = int(input("Введите: '1' -- шифр простой замены, '2' -- аффинный шифр, '3' -- аффинный рекуррентный шифр: "))

    if ch2 == 1:
        chipher_text = input("Введите текст для расшифровки: ")
        key = input("Введите ключ для расшифровки: ")
        print(decode_simple(chipher_text.lower(), key))

    elif ch2 == 2:
        language_choice = input("Выберите язык: '1' -- Ru, '2' -- En: ")
        open_text = input("Введите текст для расшифровки: ").lower()

        if language_choice == "1":  # расшифрование на русском
            # print("Список допустимых alpha: ", gcd_explore(vocab_simp))
            alpha = int(input("Введите значение alpha: "))
            # print("Список допустимых beta: ", [x for x in range(len(vocab_simp))])
            beta = int(input("Введите значение beta: "))
            print("Расшифрованный текст: ", aff_decode(vocab_simp, open_text, alpha, beta))

        elif language_choice == "2":  # шифрование на английском
            # print("Список допустимых alpha: ", gcd_explore(vocab_simp_en))
            alpha = int(input("Введите значение alpha: "))
            # print("Список допустимых beta: ", [x for x in range(len(vocab_simp))])
            beta = int(input("Введите значение beta: "))
            print("Расшифрованный текст: ", aff_decode(vocab_simp_en, open_text, alpha, beta))

    elif ch2 == 3:
        language_choice = input("Выберите язык: '1' -- Ru, '2' -- En: ")
        open_text = input("Введите текст для расшифровки: ").lower()

        if language_choice == "1":  # расшифрование на русском
            # print("Список допустимых alpha: ", gcd_explore(vocab_simp))
            alpha1 = int(input("Введите значение alpha: "))
            alpha2 = int(input("Введите значение alpha: "))
            # print("Список допустимых beta: ", [x for x in range(len(vocab_simp))])
            beta1 = int(input("Введите значение beta: "))
            beta2 = int(input("Введите значение beta: "))
            print("Расшифрованный текст: ", aff_rec_decode(open_text, vocab_simp, alpha1, alpha2, beta1, beta2))

        elif language_choice == "2":  # шифрование на английском
            # print("Список допустимых alpha: ", gcd_explore(vocab_simp))
            alpha1 = int(input("Введите значение alpha: "))
            alpha2 = int(input("Введите значение alpha: "))
            # print("Список допустимых beta: ", [x for x in range(len(vocab_simp))])
            beta1 = int(input("Введите значение beta: "))
            beta2 = int(input("Введите значение beta: "))
            print("Расшифрованный текст: ", aff_rec_decode(open_text, vocab_simp_en, alpha1, alpha2, beta1, beta2))