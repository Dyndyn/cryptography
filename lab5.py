import math
import random
from itertools import islice
from string import printable
K = 4


# 1.
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


# 2.
def prime_generator():
    i = 10
    while True:
        i += 1
        if is_prime(i, K):
            yield i


def prime_gen():
    primes = list([x for x in islice(prime_generator(), 1000)])
    return primes[random.randrange(len(primes))], primes[random.randrange(len(primes))]


def gcdex(a, b):
    if b == 0:
        return a, 1, 0
    d, x, y = gcdex(b, a % b)
    return d, y, x - (a // b) * y


def inverse_element(a, n):
    gcd, x, y = gcdex(a, n)
    # if x < 0:
    #     return x + n
    return x


def decrypt(strEncrypted, n, privKey):
    encoded = [pow(charEnc, privKey, n) for charEnc in strEncrypted]
    return ''.join([printable[char] for char in encoded])


def encrypt(str, n, pubKey):
    encoded = [printable.find(char) for char in str]
    return [pow(char, pubKey, n) for char in encoded]


print('is_prime(221, ', K, ') = ', is_prime(221, K), ', probability of false positive = ', 4 ** (-K) * 100, '%')
print('is_prime(997, ', K, ') = ', is_prime(419, K), ', probability of false positive = ', 4 ** (-K) * 100, '%')
print('is_prime(997, ', K, ') = ', is_prime(427, K), ', probability of false positive = ', 4 ** (-K) * 100, '%')
print('is_prime(997, ', K, ') = ', is_prime(997, K), ', probability of false positive = ', 4 ** (-K) * 100, '%')

str = input('Enter your message:')

print('Generating Primes..')
p, q = prime_gen()
n = p * q
print('p: ', p, 'q: ', q, 'n: ', n)

pubKey = random.randint(0, 10000)
while math.gcd(pubKey, n) != 1:
    pubKey = random.randint(0, 10000)

fi = (p - 1) * (q - 1)
privKey = inverse_element(pubKey, fi)

print('Public key:  ', pubKey)
print('Private key: ', privKey)

encrypted = encrypt(str, n, pubKey)
print('Encrypted message is:')
print(encrypted)

decrypted = decrypt(encrypted, n, privKey)
print('Decrypted message is:')
print(decrypted)
