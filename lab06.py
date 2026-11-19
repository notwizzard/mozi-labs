import argparse

from arithmetic import bezout, integer_root

M = 578287


def sieve_difference(n, moduli):
    residues = [{i*i % m for i in range(m)} for m in moduli]
    for x in range(integer_root(n)+1, (n+1)//2):
        z = x*x - n
        if any(z % m not in allowed for m, allowed in zip(moduli, residues)):
            continue
        y = integer_root(z)
        if y*y == z:
            return x, y, x-y, x+y
    return None


def rho(n, slow, fast):
    def advance(x):
        return (x*x+1) % n

    for step in range(1, n+1):
        slow = advance(slow)
        fast = advance(advance(fast))
        difference = abs(slow-fast)
        divisor = bezout(difference, n)[0]
        if divisor == n:
            return None
        if divisor > 1:
            return step, slow, fast, difference, divisor, n//divisor
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--moduli", type=int, nargs=3)
    parser.add_argument("--seeds", type=int, nargs=2)
    args = parser.parse_args()
    try:
        moduli = args.moduli or list(map(int, input("Три модуля решёт: ").split()))
        seeds = args.seeds or list(map(int, input("Два начальных значения ρ: ").split()))
        if len(moduli) != 3 or any(not 2 <= m <= M for m in moduli):
            raise ValueError("Введите три модуля от 2 до m")
        if len(seeds) != 2:
            raise ValueError("Введите два начальных значения")
    except ValueError as error:
        parser.error(str(error))
    print(f"m={M}, модули={moduli}, начальные значения={seeds}")
    result = sieve_difference(M, moduli)
    print("Решето (x, y, p, q):", result)
    result = rho(M, *seeds)
    print("ρ (шаг, медленное, быстрое, разность, НОД, второй делитель):", result)
    if result is None:
        print("ρ: выберите другие начальные значения")


if __name__ == "__main__":
    main()
