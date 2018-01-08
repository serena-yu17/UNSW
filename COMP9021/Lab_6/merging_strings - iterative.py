def seq():
    start = list(range(len1))
    yield set(start)
    pos_set = [start]
    for shift in range(len2):
        for comb in pos_set:
            for elem in range(len1 - 1, -1, -1):
                if (elem < len1 - 1 and comb[elem] + 1 < comb[elem + 1]) or (
                                elem == len1 - 1 and comb[elem] != len3 - 1):
                    comb[elem] += 1
                    pos_set.append(comb.copy())
                    yield set(comb)
    yield None


def search():
    seqs = seq()
    position = next(seqs)
    while position:
        st = list()
        p1 = 0
        p2 = 0
        for i in range(len3):
            if i in position and p1 < len1:
                st.append(s1[p1])
                p1 += 1
            else:
                if p2 < len2:
                    st.append(s2[p2])
                    p2 += 1
        if "".join(st) == s3:
            return 1
        position = next(seqs)
    return 0


s1 = input("Please input the first string: ")
s2 = input("Please input the second string: ")
s3 = input("Please input the third string: ")
len1 = len(s1)
len2 = len(s2)
len3 = len(s3)
name = "third"
if len1 > len3:
    s1, s3 = s3, s1
    len1, len3 = len3, len1
    name = "first"
if len2 > len3:
    s2, s3 = s3, s2
    len2, len3 = len3, len2
    name = "second"
if len1 > len2:
    s1, s2 = s2, s1
    len1, len2 = len2, len1
if len3 != len1 + len2:
    print("No solution")
else:
    if search():
        print(f"The {name} string can be obtained by merging the other two.")
    else:
        print("No solution")
