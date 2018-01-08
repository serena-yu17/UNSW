import sys
from itertools import permutations
from random import SystemRandom

# IO
s = input("Enter a strictly positive number for the number of couples: ")
try:
    n = int(s)
    if n <= 0:
        raise ValueError
except ValueError:
    print("Invalid input, giving up...")
    sys.exit(1)
print("Enter 4 names for the men, all on one line and separated by spaces,")
s = input("  or just press Enter for the default \"names\" M_1, ..., M_4:\n")
m_name = s.split(" ")
if len(m_name) != n:
    m_name.clear()
    for i in range(n):
        m_name.append(f"M_{i+1}")

print("Enter 4 names for the women, all on one line and separated by spaces,")
s = input("  or just press Enter for the default \"names\" W_1, ..., W_4:\n")
w_name = s.split(" ")
if len(w_name) != n:
    w_name.clear()
    for i in range(n):
        w_name.append(f"W_{i+1}")
m_pref = [None] * n
w_pref = [None] * n
print("Press Enter to get a default preference for all men or women.")
print("Otherwise, input one or more nonspace characters before Enter")
s = input("  to be prompted and enter the preferences of your choice: ")
print()
if s != "":
    for i in range(n):
        s = input(f"List preferences for {m_name[i]}, in decreasing order: ")
        s = s.split()
        if len(s) != n:
            s = ""
            break
        m_pref[i] = [None] * n
        name_dic = {}
        for j in range(n):
            name_dic[w_name[j]] = j
        for j in range(n):
            try:
                m_pref[i][j] = name_dic[s[j]]
            except KeyError:
                s = ""
                break
    print()
    for i in range(n):
        s = input(f"List preferences for {w_name[i]}, in decreasing order: ")
        s = s.split()
        if len(s) != n:
            s = None
            break
        w_pref[i] = dict()
        name_dic = {}
        for j in range(n):
            name_dic[m_name[j]] = j
        for j in range(n):
            try:
                w_pref[i][name_dic[s[j]]] = j
            except KeyError:
                s = ""
                break
if s == "":
    perm = list(permutations(list(range(n)), n))
    perm_count = len(perm) - 1
    rnd = SystemRandom()
    m_rnd = []
    used = set()
    for i in range(n):
        n_perm = rnd.randint(0, perm_count // 2)
        while n_perm in used:
            n_perm = rnd.randint(0, perm_count // 2)
        m_rnd.append(n_perm * 2)
        used.add(n_perm)
    w_rnd = []
    used.clear()
    for i in range(n):
        n_perm = rnd.randint(0, perm_count // 2 - 1)
        while n_perm in used:
            n_perm = rnd.randint(0, perm_count // 2 - 1)
        w_rnd.append(n_perm * 2 + 1)
        used.add(n_perm)
    for i in range(n):
        m_pref[i] = list(perm[m_rnd[i]])
        print(f"Preferences for {m_name[i]}: ", end="")
        for j in range(n):
            print(w_name[m_pref[i][j]], end=" ")
        print()
    print()
    for i in range(n):
        pref = perm[w_rnd[i]]
        print(f"Preferences for {w_name[i]}: ", end="")
        w_pref[i] = dict()
        for j in range(n):
            w_pref[i][pref[j]] = j
            print(m_name[pref[j]], end=" ")
        print()
    print()
# end IO
for i in range(n):
    m_pref[i].reverse()  # for convenience of pop
done = 0
m_select = [None] * n
w_select = [None] * n
for i in range(n):
    w_select[i] = set()
while done == 0:
    # select
    for i in range(n):
        if m_select[i] is None and len(m_pref[i]) > 0:
            chosen_w = m_pref[i].pop()
            m_select[i] = chosen_w
            w_select[chosen_w].add(i)
    done = 1
    # reject
    for i in range(n):
        if w_select[i] is not None and len(w_select[i]) > 1:
            chosen_m = sorted(w_select[i], key=lambda x: w_pref[i][x])
            done = 0
            for j in range(1, len(chosen_m)):
                w_select[i].remove(chosen_m[j])
                m_select[chosen_m[j]] = None
pairs = []
for i in range(n):
    if w_select[i] is not None:
        m_id = tuple(w_select[i])[0]
        pairs.append((w_name[i], m_name[m_id]))
pairs.sort()
for line in pairs:
    print(line[0], "--", line[1])
