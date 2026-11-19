from arithmetic import integer_root, inverse, power_mod

E, N, CIPHERTEXT = 59, 28829, 16357


def classroom_example():
    p = next(d for d in range(2, integer_root(N)+1) if N % d == 0)
    q = N // p
    phi = (p-1)*(q-1)
    d = inverse(E, phi)
    message = power_mod(CIPHERTEXT, d, N)
    assert power_mod(message, E, N) == CIPHERTEXT
    return p, q, phi, d, message


if __name__ == "__main__":
    p, q, phi, d, message = classroom_example()
    print(f"n = {N} = {p} × {q}\ne = {E}, φ = {phi}, d = {d}")
    print(f"C = {CIPHERTEXT}, M = {message}")
