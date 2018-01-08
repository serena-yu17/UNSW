ub = input("Input the upper limit to scan: ")
ub = int(ub)
L_prime = [1] * ub
L_prime[0] = 0
L_prime[1] = 0
for i in range(2, int(ub ** 0.5 + 1)):
    if L_prime[i] == 1:
        j = i + 1
        while i * j < ub:
            L_prime[i * j] = 0
            j += 1
pattern = [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
select = []
for a in range(2, ub):
    flag = 1
    for i in range(31):
        if L_prime[i + a] != pattern[i]:
            flag = 0
            break
    if flag == 1:
        select.append((a, a + 2, a + 6, a + 12, a + 20, a + 30))
for tup in select:
    print(*tup)
