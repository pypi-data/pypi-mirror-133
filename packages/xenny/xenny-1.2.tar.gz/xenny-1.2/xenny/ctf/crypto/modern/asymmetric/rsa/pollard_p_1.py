from Crypto.Util.number import long_to_bytes
from gmpy2 import powmod, gcd

def pollard(N, t):
    a = 2
    n = 2
    while True:
        a = powmod(a, n, N)
        p = gcd(a-1, N)
        if p != 1 and p != N:
            return p
        n += 1


def attack(n, timeout=60):
    return pollard(n, timeout)