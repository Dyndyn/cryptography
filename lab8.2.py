import random
from itertools import islice
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


def generatePublicAndPrivateKeys():
    n = prime_gen()

    g = random.randrange(1, n)
    a = random.randrange(2, n - 1)
    h = pow(g, a, n)

    return {
               "n": n,
               "g": g,
               "h": h
           }, {  # private
               "n": n,
               "a": a
           }


def encrypt(numb):
    n = pub["n"]
    g = pub["g"]
    h = pub["h"]

    r = random.randrange(2, n - 1)

    c1 = pow(g, r, n)
    c2 = (numb * pow(h, r, n)) % n

    return c1, c2


def decrypt(c1, c2):
    n = priv["n"]
    a = priv["a"]

    numb = c2 * pow(pow(c1, a, n), n - 2, n) % n
    return numb


str = int(input('Enter number to be encrypted:'))

pub, priv = generatePublicAndPrivateKeys()
print('Public key:  ', pub)
print('Private key: ', priv)

c1, c2 = encrypt(str)

decrypted = decrypt(c1, c2)

print('Encrypted number is:')
print('c1 :', c1)
print('c2 :', c2)

print('Decrypted number is:', decrypted)