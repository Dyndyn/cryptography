import math


# 1.
def gcdex(a, b):
    if b == 0:
        return a, 1, 0
    d, x, y = gcdex(b, a % b)
    return d, y, x - (a // b) * y


# 2.
def inverse_element(a, n):
    gcd, x, y = gcdex(a, n)
    return x


# 3.
def phi(n):
    result = n

    # Розглядаємо всі прості дільники n
    # і віднімаємо їх множники з результату
    p = 2
    while p * p <= n:

        # перевіряємо чи p є простим дільником.
        if n % p == 0:

            # Якщо так, то оновлюємо n та результат
            while n % p == 0:
                n = int(n / p)
            result -= int(result / p)
        p += 1

    # Якщо n має дільник більший за корінь квадратний n
    # тоді такий дільник може бути тільки один
    if n > 1:
        result -= int(result / n)
    return result


# 4.
def inverse_element_2(a, m):
    k = 1
    while (m * k + 1) % a:
        k += 1
    return int((m * k + 1) / a)


print('gcdex(612, 342) = ', gcdex(612, 342))
print('inverse_element(5, 18) = ', inverse_element(5, 18))
print('phi(16) = ', phi(16))
print('inverse_element_2(5, 18) = ', inverse_element_2(5, 18))
