import argparse
from pathlib import Path

from arithmetic import ALPHABET

CIPHERTEXT = "кшюбхшэребхшюыэбюшвабребъхжкыецбгчб"


def shift(text, key):
    rotated = ALPHABET[key % 32:] + ALPHABET[:key % 32]
    return text.translate(str.maketrans(
        ALPHABET + ALPHABET.upper() + 'ёЁ',
        rotated + rotated.upper() + rotated[5] + rotated[5].upper(),
    ))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", nargs="?", default="variant", choices=["variant", "encrypt", "decrypt"])
    parser.add_argument("--key", type=int, choices=range(1, 32))
    parser.add_argument("--output", type=Path, default=Path("lab01_results.txt"))
    args = parser.parse_args()
    if args.mode == "variant":
        rows = [f"Шифртекст: {CIPHERTEXT}"]
        rows.extend(f"{k:02}: {shift(CIPHERTEXT, -k)}" for k in range(1, 32))
        title = "горькийнадне"
        rows.extend(["Ключ: 19", "Автор и произведение: Максим Горький, «На дне»",
                     f"Фамилия и название в шифре: {shift(title, 19)}"])
    else:
        if args.key is None:
            parser.error("укажите --key")
        sign = 1 if args.mode == "encrypt" else -1
        rows = [f"Ключ {args.key}: {shift(input('Текст: '), sign * args.key)}"]
    result = "\n".join(rows) + "\n"
    with args.output.open("a" if args.mode == "decrypt" else "w", encoding="utf-8") as file:
        file.write(result)
    print(result, end="")


if __name__ == "__main__":
    main()
