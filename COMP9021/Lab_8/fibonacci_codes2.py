

def fib(ub=65535, length=65535):
    fibo = list()
    fibo.append(0)
    fibo.append(1)
    i = 2
    while fibo[-1] < ub + 1 and i < length + 3:
        fibo.append(fibo[i-1] + fibo[i-2])
        i += 1
    return fibo[2:]

def search(target, fibo, cur_sum, used):
    if cur_sum == target:
        return used
    if cur_sum < target:
        i =  used[-1] - 1
        while fibo[i] > target - cur_sum:
            i -= 1
        found = None
        while not found and i >= 0:
            found = search(target, fibo, cur_sum + fibo[i], used + [i])
            i -= 1
        return found

def encode(n):
    fibo = fib(ub=n)
    found = None
    i = len(fibo) - 1
    while not found and i >= 0:
        found = search(n, fibo, fibo[i], [i])
        i -= 1
    if not found:
        return ""
    code = list()
    #print(fibo, found)
    code_set = set(found)
    for i in range(found[0] + 1):
        if i in code_set:
            code.append('1')
        else:
            code.append('0')
    code.append('1')
    return ''.join(code)
    
def decode(st):
    fibo = fib(length=len(st))
    #print(fibo)
    sum = 0
    for i in range(len(st) - 1):
        if st[i] == '1':
            sum += fibo[i]
    return sum
    
