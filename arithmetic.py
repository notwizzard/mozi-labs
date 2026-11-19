def bezout(a, b):
    r, s = abs(a), abs(b)
    x, u, y, v = 1, 0, 0, 1
    while s:
        q, rem = divmod(r, s)
        r, s = s, rem
        x, u = u, x - q * u
        y, v = v, y - q * v
    return r, x if a >= 0 else -x, y if b >= 0 else -y


def inverse(a, m):
    if m < 2:
        raise ValueError("Модуль должен быть не меньше 2")
    g, x, _ = bezout(a, m)
    if g != 1:
        raise ValueError(f"Обратного элемента нет: НОД = {g}")
    return x % m


def power_mod(base, exponent, modulus):
    if exponent < 0 or modulus < 1:
        raise ValueError("Нужны неотрицательная степень и положительный модуль")
    value = 1 % modulus
    base %= modulus
    while exponent:
        if exponent & 1:
            value = (value * base) % modulus
        base = base * base % modulus
        exponent >>= 1
    return value


def integer_root(n):
    if n < 0:
        raise ValueError("Корень определён для n ≥ 0")
    if n < 2:
        return n
    x = n
    while (y := (x + n // x) // 2) < x:
        x = y
    return x


ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"


def russian_letters(text):
    return ''.join(c for c in text.lower().replace('ё', 'е') if c in ALPHABET)
