from arithmetic import integer_root, power_mod

A, B, P = 2, 12161, 30203


def baby_giant(a, b, p):
    k = integer_root(p)+1
    giant = power_mod(a, k, p)
    y, z = 1, b % p
    baby = {}
    for j in range(k):
        baby.setdefault(z, j)
        z = z*a % p
    for i in range(k+1):
        if y in baby:
            j = baby[y]
            x = i*k-j
            if x >= 0 and power_mod(a, x, p) == b % p:
                return k, i, j, y, x
        y = y*giant % p
    return None


if __name__ == "__main__":
    k, i, j, residue, log = baby_giant(A, B, P)
    print(f"a={A}, b={B}, p={P}, k={k}")
    print(f"i={i}, j={j}, y_i=z_j={residue}, x={log}")
    print(f"Проверка: {A}^{log} mod {P} = {power_mod(A, log, P)}")
