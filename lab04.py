import argparse

from arithmetic import ALPHABET, bezout, inverse, power_mod

P, Q = 101, 233
N = P * Q
PHI = (P - 1) * (Q - 1)
CODES = {letter: str(i) for i, letter in enumerate(ALPHABET.upper(), 10)}
CODES[" "] = "99"
LETTERS = {code: letter for letter, code in CODES.items()}


def key_pairs(phi):
    pairs = []
    for e in range(2, phi):
        if bezout(e, phi)[0] == 1:
            pairs.append((e, inverse(e, phi)))
            if len(pairs) == 3:
                return pairs
    raise ValueError("Меньше трёх допустимых показателей")


def encode(text):
    try:
        return ''.join(CODES[c] for c in text.upper().replace('Ё', 'Е'))
    except KeyError as error:
        raise ValueError(f"Недопустимый символ: {error.args[0]!r}") from error


def split_blocks(digits, modulus):
    blocks = []
    while digits:
        for length in range(min(len(digits), len(str(modulus-1))), 0, -1):
            head, tail = digits[:length], digits[length:]
            if head[0] != '0' and int(head) < modulus and not tail.startswith('0'):
                blocks.append(int(head))
                digits = tail
                break
        else:
            raise ValueError("Далее нельзя выделить блок без начального нуля")
    return blocks


def decode(blocks):
    digits = ''.join(map(str, blocks))
    if len(digits) % 2:
        raise ValueError("Некорректная длина строки кодов")
    return ''.join(LETTERS[digits[i:i+2]] for i in range(0, len(digits), 2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text")
    parser.add_argument("--key", type=int, choices=(1, 2, 3))
    args = parser.parse_args()
    keys = key_pairs(PHI)
    print(f"p={P}, q={Q}, n={N}, φ={PHI}")
    for i,(e,d) in enumerate(keys, 1):
        print(f"{i}. Открытый ({e}, {N}), закрытый ({d}, {N})")
    try:
        text = args.text if args.text is not None else input("Текст: ")
        index = args.key if args.key is not None else int(input("Выберите ключ 1–3: "))
        if index not in (1, 2, 3):
            raise ValueError("Ключ должен быть от 1 до 3")
        e, d = keys[index-1]
        blocks = split_blocks(encode(text), N)
        ciphertext = [power_mod(block, e, N) for block in blocks]
        decrypted = decode([power_mod(block, d, N) for block in ciphertext])
        print(f"Текст: {text}\nБлоки: {blocks}\nШифртекст: {ciphertext}\nРасшифровка: {decrypted}")
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
