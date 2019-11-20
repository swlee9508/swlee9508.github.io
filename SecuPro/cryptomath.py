# Cryptomath Module

def gcd(a, b):
    # Return the GCD of a and b using Euclid's Algorithm
    while a != 0:
        a, b = b % a, a
    return b


def findModInverse(a, m):
    if gcd(a, m) != 1:
        return None # no mod inverse if a & m aren't relatively prime

    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3 # // is the integer division operator
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return None
    else:
        return x % m

def multinv(value, modulus):
    x, lastx = 0, 1
    a, b = modulus, value
    while b:
        a, q, b = b, a // b, a % b
        x, lastx = lastx - q * x, x
    result = (1 - lastx * modulus) // value
    if result < 0:
        result += modulus
    assert 0 <= result < modulus and value * result % modulus == 1
    return result

def multiplicativeInverse(x, modulus):
    if modulus <= 0:
       raise ValueError("modulus must be positive")

    a = abs(x)
    b = modulus
    sign = -1 if x < 0 else 1

    c1 = 1
    d1 = 0
    c2 = 0
    d2 = 1

    # Loop invariants:
    # c1 * abs(x) + d1 * modulus = a
    # c2 * abs(x) + d2 * modulus = b

    while b > 0:
        q = a / b
        r = a % b
        # r = a - qb.

        c3 = c1 - q*c2
        d3 = d1 - q*d2

        # Now c3 * abs(x) + d3 * modulus = r, with 0 <= r < b.

        c1 = c2
        d1 = d2
        c2 = c3
        d2 = d3
        a = b
        b = r

    if a != 1:
        raise ValueError("gcd of %d and %d is %d, so %d has no "
                         "multiplicative inverse modulo %d"
                         % (x, modulus, a, x, modulus))

    return c1 * sign