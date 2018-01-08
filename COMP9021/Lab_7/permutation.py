
def rev(lst, begin, end):
    while begin < end:
        lst[begin], lst[end] = lst[end], lst[begin]
        begin += 1
        end -= 1

def perm(lst):
    leng = len(lst)
    i = leng - 1
    while 1:
        j = i
        i -= 1
        if lst[i] < lst[j]:
            k = leng
            while lst[i] >= lst[k - 1]:
                k -= 1
            k -= 1
            lst[i], lst[k] = lst[k], lst[i]
            rev(lst, j, leng - 1)
            return 1
        if i == 0:
            lst.reverse()
            return 0


lst = [1, 2, 3, 4, 5]
while perm(lst):
    print(lst)
