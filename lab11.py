import random

from collections import namedtuple


def invert(n, q):
    return extendedGCD(n, q) % q


def extendedGCD(a, b):
    s0, s1, t0, t1 = 1, 0, 0, 1
    while b > 0:
        q, r = divmod(a, b)
        a, b = b, r
        s0, s1, t0, t1 = s1, s0 - q * s1, t1, t0 - q * t1
    return s0


def getElypcitCurve(a, b, q):
    if 0 < a and 0 < b and a < q and b < q and 2 < q and ((4 * (a ** 3) + 27 * (b ** 2)) % q) != 0:
        return {
            "a": a,
            "b": b,
            "q": q,
            "zero": anPoint(0, 0)
        }
    raise ValueError('Wrong params for getElypcitCurve')


def isValidOnElypcitCurve(point):
    if point == elypcitCurve["zero"]:
        return True
    l = (point.y ** 2) % elypcitCurve["q"]
    r = ((point.x ** 3) + elypcitCurve["a"] * point.x + elypcitCurve["b"]) % elypcitCurve["q"]
    return l == r


def getPontsOnElypcitCurveFor(x):
    ysq = (x ** 3 + elypcitCurve["a"] * x + elypcitCurve["b"]) % elypcitCurve["q"]

    for i in range(1, elypcitCurve["q"]):
        if i * i % elypcitCurve["q"] == ysq:
            y, my = i, elypcitCurve["q"] - i

    return anPoint(x, y), anPoint(x, my)


def negPointOnElypcitCurve(p):
    return anPoint(p.x, -p.y % elypcitCurve["q"])


def addPointsOnElypcitCurve(p1, p2):
    if p1 == elypcitCurve["zero"]: return p2
    if p2 == elypcitCurve["zero"]: return p1
    if p1.x == p2.x and (p1.y != p2.y or p1.y == 0):
        return elypcitCurve["zero"]
    if p1.x == p2.x:
        l = (3 * p1.x * p1.x + elypcitCurve["a"]) * invert(2 * p1.y, elypcitCurve["q"]) % elypcitCurve["q"]
    else:
        l = (p2.y - p1.y) * invert(p2.x - p1.x, elypcitCurve["q"]) % elypcitCurve["q"]
    x = (l * l - p1.x - p2.x) % elypcitCurve["q"]
    y = (l * (p1.x - x) - p1.y) % elypcitCurve["q"]
    return anPoint(x, y)


def muliptyPointsOnElypcitCurve(p, n):
    r = elypcitCurve["zero"]
    m2 = p
    while 0 < n:
        if n & 1 == 1:
            r = addPointsOnElypcitCurve(r, m2)
        n, m2 = n >> 1, addPointsOnElypcitCurve(m2, m2)
    return r


def orderOfPointOnElypcitCurve(g):
    if isValidOnElypcitCurve(g) and g != elypcitCurve["zero"]:
        for i in range(1, elypcitCurve["q"] + 1):
            if muliptyPointsOnElypcitCurve(g, i) == elypcitCurve["zero"]:
                return i


anPoint = namedtuple("Dot", ["x", "y"])
predecidedNumber = 7

elypcitCurve = getElypcitCurve(1, 18, 19)
g, _ = getPontsOnElypcitCurveFor(predecidedNumber)
n = orderOfPointOnElypcitCurve(g)


def getPubElGamal(priv, g):
    return muliptyPointsOnElypcitCurve(g, priv)


def encryptElGamal(plain, pub, g, r):
    if isValidOnElypcitCurve(plain) and isValidOnElypcitCurve(pub):
        return (muliptyPointsOnElypcitCurve(g, r), addPointsOnElypcitCurve(plain, muliptyPointsOnElypcitCurve(pub, r)))


def decryptElGamal(c1, c2, priv):
    if isValidOnElypcitCurve(c1) and isValidOnElypcitCurve(c2):
        return addPointsOnElypcitCurve(c2, negPointOnElypcitCurve(muliptyPointsOnElypcitCurve(c1, priv)))


mapping = [muliptyPointsOnElypcitCurve(g, i) for i in range(n)]
plain = mapping[predecidedNumber]
print('Initial value:', plain)

privateKey = random.randrange(2, 18)
publicKey = getPubElGamal(privateKey, g)

print('Public key:  ', publicKey)
print('Private key: ', privateKey)
print()

c1, c2 = encryptElGamal(plain, publicKey, g, random.randrange(2, 18))
numb = decryptElGamal(c1, c2, privateKey)
print('Decrypted dot c1:', c1)
print('Decrypted dot c2:', c2)
print('Decrypted:', numb)