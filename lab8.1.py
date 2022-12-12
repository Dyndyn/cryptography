import random
from itertools import islice
K = 4


def is_prime(n, k):
    if n % 2 == 0:
        return False
    for i in range(k):
        witness = random.randint(2, n-2)
        s = 0
        copy_n = n - 1
        while copy_n % 2 == 0:
            s += 1
            copy_n /= 2
        d = int((n-1) / 2 ** s)
        x = pow(witness, d, n)
        y = 1
        for j in range(s):
            y = pow(x, 2, n)
            if y == 1 and x != 1 and x != n-1:
                return False
            x = y
        if y != 1:
            return False
    return True


def prime_generator():
    i = 10
    while True:
        i += 1
        if is_prime(i, K):
            yield i


def prime_gen():
    primes = list([x for x in islice(prime_generator(), 1000)])
    return primes[random.randrange(len(primes))]


def is_primitive_root(g, p):
    for i in range(1, p-1):
        if pow(g, i, p) == 1:
            return False
    return True


def get_g(p):
    while True:
        g = random.randint(2, p)
        if is_primitive_root(g, p):
            return g


prime = prime_gen()
g = get_g(prime)

user1PrivateKey = random.getrandbits(32)
user1PubicKey = pow(g, user1PrivateKey, prime)

user2PrivateKey = random.getrandbits(32)
user2PubicKey = pow(g, user2PrivateKey, prime)

user1Shared = pow(user2PubicKey, user1PrivateKey, prime)
user2Shared = pow(user1PubicKey, user2PrivateKey, prime)

print("g: ", g)
print("p: ", prime)
print("User 1:")
print("     Private key:", user1PrivateKey)
print("     Public key:", user1PubicKey)
print("     Side 1 has Digital signature of side 2:", user1Shared)

print("User 2:")
print("     Private key:", user2PrivateKey)
print("     Public key:", user2PubicKey)
print("     Side 2 has Digital signature of side 1:", user2Shared)
