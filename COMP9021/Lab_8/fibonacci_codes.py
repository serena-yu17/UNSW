import sys


def genfib(count=None, ub=None):
    if not count and not ub:
        return None
    if not ub:
        ub = sys.maxsize
    if not count:
        count = sys.maxsize
    fib = [0, 1]
    i = 2
    while i <= count:
        fib.append(fib[i - 1] + fib[i - 2])
        if fib[i] > ub:
            break
        i += 1
    return fib


def encode(n):
    if n <= 0:
        return ""
    fib = genfib(ub=n)
    encoding = ['0'] * (len(fib) - 3)
    for i in range(len(fib) - 2, 1, -1):
        if n >= fib[i]:
            n -= fib[i]
            encoding[i - 2] = '1'
        if n == 0:
            break
    encoding.append('1')
    return "".join(encoding)


def decode(st):
    if len(st) == 1 or st[len(st) - 1] == 0:
        return 0
    num = []
    for i in range(len(st) - 1):
        num.append(st[i])
        if i > 0 and num[i] == '1' and num[i - 1] == '1':
            return 0
    sm = 0
    fib = genfib(count=len(num) + 2)
    for i in range(len(num)):
        if num[i] == '1':
            sm += fib[i + 2]
    return sm


print(encode(12))
print(decode('100011011'))
print(decode('1011'))
print(decode('1000011'))