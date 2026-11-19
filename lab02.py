import argparse
from collections import Counter
from pathlib import Path

from arithmetic import ALPHABET, bezout, inverse, russian_letters

CIPHERTEXT = (
    "щгзшмпвжгщгзфвлыоцунпыщумжгфбгъгйвщйртжыпыщщгзъгъвйвпн"
    "здтпнунхбгтжфвпдъвйыпгъъдтийвувоыицмлбгщгзъгбмучытънхбгтжщны"
    "щцвинбнъцвипйвуво"
)
FREQUENCY_ORDER = "оеаитнсрвлкмдпуяызъьбгчйхжюшцщэф"


def congruence(a, b, m):
    if m < 2:
        raise ValueError("Модуль должен быть не меньше 2")
    g, coefficient, _ = bezout(a, m)
    if b % g:
        return []
    step = m // g
    first = (coefficient * (b // g)) % step
    return [first + k * step for k in range(g)]


def system(a, b, c, d, m):
    return [(x, (b - a*x) % m) for x in congruence(a-c, b-d, m)]


def decrypt(ciphertext, a, b):
    inv = inverse(a, 32)
    return ''.join(ALPHABET[inv * (ALPHABET.index(c) - b) % 32]
                   for c in russian_letters(ciphertext))


def hypotheses(ciphertext):
    counts = Counter(russian_letters(ciphertext))
    if len(counts) < 2:
        raise ValueError("Для двух сравнений нужны две различные буквы")
    (first, _), (second, _) = counts.most_common(2)
    order = list(dict.fromkeys(FREQUENCY_ORDER + ALPHABET))
    seen = set()
    for x in order:
        for y in order:
            if x == y:
                continue
            for key in system(ALPHABET.index(x), ALPHABET.index(first),
                              ALPHABET.index(y), ALPHABET.index(second), 32):
                if key[0] % 2 and key not in seen:
                    seen.add(key)
                    yield x, y, key


def run_variant(output, step):
    counts = Counter(CIPHERTEXT)
    total = sum(counts.values())
    first, second = [c for c, _ in counts.most_common(2)]
    with output.open("w", encoding="utf-8") as file:
        def record(line):
            print(line)
            file.write(line + "\n")

        record(f"Шифртекст: {CIPHERTEXT}")
        record("Частоты: " + " ".join(f"{c}={counts[c]}/{total}" for c in ALPHABET))
        record(f"Две наиболее частые буквы: {first}, {second}")
        for x, y, key in hypotheses(CIPHERTEXT):
            record(f"{x}→{first}, {y}→{second}; ключ {key}: {decrypt(CIPHERTEXT, *key)}")
            if step and input("Enter — дальше, q — остановиться: ").strip().lower() == "q":
                return
        if not step:
            record(f"Выбранный ключ (19, 3): {decrypt(CIPHERTEXT, 19, 3)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", nargs="?", default="variant",
                        choices=["variant", "inverse", "congruence", "system"])
    parser.add_argument("--step", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("lab02_results.txt"))
    args = parser.parse_args()
    try:
        if args.mode == "variant":
            run_variant(args.output, args.step)
        elif args.mode == "inverse":
            print(inverse(*map(int, input("a m: ").split())))
        elif args.mode == "congruence":
            print(congruence(*map(int, input("a b m: ").split())))
        else:
            print(system(*map(int, input("a b c d m: ").split())))
    except (TypeError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
