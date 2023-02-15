import math

vocab_simp = list('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')# полный русский алфавит
vocab_simp_en = list('abcdefghijklmnopqrstuvwxyz')# полный английский алфавит

def gcd_explore(alphabet):
    vocab_simp = list(alphabet)
    m = len(vocab_simp)
    gcd = []
    for i in range(1, m + 1):
        if math.gcd(i, m) == 1:
            gcd.append(i)
    return gcd


def alpha_inverse(a, p):
    for d in range(1, p):
        r = (d * a) % p
        if r == 1:
            break
    else:
        raise ValueError('%d has no inverse mod %d' % (a, p))
    return d

def aff_decode(alphabet, cipher_text, alpha, beta):
    open_txt = ''
    alpha_inv = alpha_inverse(alpha, len(alphabet))
    for i in cipher_text:  # цикл пропускает все пробелы, чтобы их не шифровать
        if i == ' ' or i == ',' or i == "." or i == ':' or i == ";":
            open_txt += i
            continue
        open_txt += alphabet[(alpha_inv * (alphabet.index(i) - beta)) % len(alphabet)]
    return open_txt

def analiz_bigramm(text):
    """
       функция считает количество вхождений подстрок в исходный текст
       :param text: исходный текст
       :return: количество вхождений
       """
    bigr = ['ст', 'но', 'ен', 'то', 'на', 'ов', 'ни', 'ра', 'во', 'ко', 'сто', 'ено', 'нов', 'тов', 'ово', 'ова']
    count = 0

    for i in range(len(bigr)):
        count += text.count(bigr[i])
    return count


message = ['', '', '']
maxi = 0
strings = []
encode_text = input('Текст: ')
lang = ''
if encode_text[0] in vocab_simp:
    lang = vocab_simp
else:
    lang = vocab_simp_en
arr_alpha = gcd_explore(lang)
arr_beta = [x for x in range(len(vocab_simp))]
for a in arr_alpha:
    for b in arr_beta:
        decode_text = aff_decode(lang, encode_text, a, b)
        m = analiz_bigramm(decode_text)

        if m > maxi:
            maxi = m
            message[0], message[1], message[2] = decode_text, a, b
print(message[0])
print(f'a={message[1]},b={message[2]}')