from random import randrange


def chunks(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]


def leftRotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xffffffff


def getShiftedMessage(data):
    bytes = ""

    h = [
        0x67452301,
        0xEFCDAB89,
        0x98BADCFE,
        0x10325476,
        0xC3D2E1F0,
    ]

    for n in range(len(data)):
        bytes += '{0:08b}'.format(ord(data[n]))
    bits = bytes + "1"
    padedBits = bits

    while len(padedBits) % 512 != 448:
        padedBits += "0"

    padedBits += '{0:064b}'.format(len(bits) - 1)

    for c in chunks(padedBits, 512):
        words = chunks(c, 32)
        w = [0] * 80
        for n in range(0, 16):
            w[n] = int(words[n], 2)
        for i in range(16, 80):
            w[i] = leftRotate((w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]), 1)

        a, b, c, d, e = h[0], h[1], h[2], h[3], h[4]

        for i in range(80):
            if i <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            a, b, c, d, e = ((leftRotate(a, 5) + f + e + k + w[i]) & 0xffffffff, a, leftRotate(b, 30), c, d)

        h[0] = (h[0] + a) & 0xffffffff
        h[1] = (h[1] + b) & 0xffffffff
        h[2] = (h[2] + c) & 0xffffffff
        h[3] = (h[3] + d) & 0xffffffff
        h[4] = (h[4] + e) & 0xffffffff

    return '%08x%08x%08x%08x%08x' % (h[0], h[1], h[2], h[3], h[4])


def isPrime(num):
    if (num >= 3):
        if (num & 1 != 0):
            r = num - 1
            u = 0
            while (r & 1) == 0:
                u += 1
                r = r // 2

            for i in range(11):
                aa = randrange(2, num - 1)
                z = pow(aa, r, num)

                if z != 1 and z != num - 1:
                    for j in range(u - 1):
                        if z != num - 1:
                            z = pow(z, 2, num)
                            if z == 1:
                                return False
                        else:
                            break
                    if z != num - 1:
                        return False
            return True
    return False


def invert(n, q):
    return extendedGCD(n, q) % q


def extendedGCD(a, b):
    s0, s1, t0, t1 = 1, 0, 0, 1
    while b > 0:
        q, r = divmod(a, b)
        a, b = b, r
        s0, s1, t0, t1 = s1, s0 - q * s1, t1, t0 - q * t1
    return s0


def generatePAndQ(L, N):
    g = N  # >= 160
    n = (L - 1) // g
    b = (L - 1) % g

    while True:
        s = randrange(1, 2 ** (g))
        a = getShiftedMessage([str(int(x)) for x in bin(s)[2:]])
        zz = (s + 1) % (2 ** g)
        z = getShiftedMessage([str(int(x)) for x in bin(zz)[2:]])
        U = int(a, 16) ^ int(z, 16)
        mask = 2 ** (N - 1) + 1
        q = U | mask
        if isPrime(q):
            break
    # print("q = ", q)
    i = 0
    j = 2
    while i < 4096:
        V = []
        for k in range(n + 1):
            arg = (s + j + k) % (2 ** g)
            zzv = getShiftedMessage([str(int(x)) for x in bin(arg)[2:]])
            V.append(int(zzv, 16))
        W = 0
        for qq in range(0, n):
            W += V[qq] * 2 ** (160 * qq)
        W += (V[n] % 2 ** b) * 2 ** (160 * n)
        X = W + 2 ** (L - 1)
        c = X % (2 * q)
        p = X - (c - 1)
        if p >= 2 ** (L - 1):
            if isPrime(p):
                # print("p = ", p)
                return p, q
        i += 1
        j += n + 1


def generateH(p, q):
    while True:
        h = randrange(2, p - 1)
        exp = (p - 1) // q
        g = pow(h, exp, p)
        if g > 1:
            break
    return g


def generateKeys(h, p, q):
    a = randrange(2, q)
    b = pow(h, a, p)
    return a, b


def generateParams(L, N):
    p, q = generatePAndQ(L, N)
    h = generateH(p, q)
    return p, q, h


def signMessage(M, p, q, h, a):
    k = randrange(2, q)
    s1 = pow(h, k, p) % q
    m = int(getShiftedMessage(M), 16)
    s2 = (invert(k, q) * (m + a * s1)) % q
    return s1, s2


def verifySign(M, s1, s2, p, q, h, b):
    if s1 < 0 and s1 > q and s2 < 0 and s2 > q:
        return False

    w = invert(s2, q)
    m = int(getShiftedMessage(M), 16)
    u1 = (m * w) % q
    u2 = (s1 * w) % q
    t = (pow(h, u1, p) * pow(b, u2, p)) % p % q
    if t == s1:
        return True
    return False


msg = input('Enter message:')

N = 160
L = 1024
p, q, h = generateParams(L, N)
a, b = generateKeys(h, p, q)

print('Parameters:')
print('* p:', p)
print('* q:', q)
print('* h:', h)
print('* b:', b)
print('* a:', a)
print()

s1, s2 = signMessage(msg, p, q, h, a)
print('Signed message:')
print("s1: " + str(s1))
print("s2: " + str(s2))

if verifySign(msg, s1, s2, p, q, h, b):
    print('Sign has been approved')
else:
    print('Sign has NOT been approved')