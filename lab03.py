import argparse
from collections import Counter
from math import log2
from pathlib import Path

from arithmetic import russian_letters

VARIANT = (
    "Гул затих. Я вышел на подмостки. Прислонясь к дверному косяку, "
    "Я ловлю в далеком отголоске, Что случится на моем веку. На меня наставлен "
    "сумрак ночи Тысячью биноклей на оси. Если только можно, Авва Отче, "
    "Чашу эту мимо пронеси."
)


def entropy(text, k):
    windows = len(text) - k + 1
    if k < 1 or windows < 1:
        raise ValueError("Требуется 1 ≤ k ≤ длины текста")
    counts = Counter(text[i:i+k] for i in range(windows))
    return -sum((count / windows) * log2(count / windows) for count in counts.values())


def plot(values, output):
    top = max(1, max(values))
    xs = [70 + i*105 for i in range(5)]
    ys = [260 - 210*value/top for value in values]
    points = ' '.join(f'{x},{y:.2f}' for x,y in zip(xs, ys))
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="550" height="320" viewBox="0 0 550 320">',
             '<rect width="550" height="320" fill="white"/>',
             '<g font-family="sans-serif" font-size="13" fill="black">',
             '<text x="70" y="25">Энтропия на букву, бит</text>',
             '<path d="M55 45 V260 H515" fill="none" stroke="black"/>',
             f'<polyline points="{points}" fill="none" stroke="#2855a6" stroke-width="2"/>']
    for i, (x, y, value) in enumerate(zip(xs, ys, values), 1):
        parts.extend([f'<circle cx="{x}" cy="{y:.2f}" r="4" fill="#2855a6"/>',
                      f'<text x="{x}" y="{y-10:.2f}" text-anchor="middle">{value:.3f}</text>',
                      f'<text x="{x}" y="281" text-anchor="middle">{i}</text>'])
    parts.append('<text x="515" y="281">k</text></g></svg>')
    output.write_text('\n'.join(parts), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", default=VARIANT)
    parser.add_argument("--output", type=Path, default=Path("lab03_entropy.svg"))
    args = parser.parse_args()
    text = russian_letters(args.text)
    if len(text) < 5:
        parser.error("Нужно минимум пять русских букв")
    values = []
    print(f"Букв: {len(text)}")
    print("k | Окон | H(k) | H(k)/k")
    for k in range(1, 6):
        value = entropy(text, k)
        values.append(value/k)
        print(f"{k} | {len(text)-k+1} | {value:.6f} | {value/k:.6f}")
    plot(values, args.output)


if __name__ == "__main__":
    main()
