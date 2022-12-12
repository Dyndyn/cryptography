import hashlib


def chunks(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]


def leftRotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xffffffff


def hash(data):
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


message = input('Enter message:')
encrypted = hash(message)
print('Hash :', encrypted)

h = hashlib.new('sha1')
h.update(message.encode())
print('Python hash realization: ', h.hexdigest())