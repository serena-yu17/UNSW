##
##
delta = 0.0001


##

def gcd(a, b):
    if a == b:
        return a
    if a < b:
        a, b = b, a
    while b > 0:
        a, b = b, a % b
    return a


class frac:
    def __init__(self, n1, n2):
        if n1 == 0:
            self.num1 = 0
            self.num2 = 0
            self.value = 0
        else:
            gd = gcd(n1, n2)
            self.num1 = n1 // gd
            self.num2 = n2 // gd
            self.value = n1 / n2
        self.minus_half = abs(self.value - 0.5)

    def __eq__(self, other):
        return self.num1 == other.num1 and self.num2 == other.num2

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __repr__(self):
        if self.num1 == 1 and self.num2 == 1:
            return '1'
        elif self.num1 == 0:
            return '0'
        else:
            return f"{self.num1}/{self.num2}"


def list_frac(L):
    L_frac = []
    if len(L) == 1:
        new_frac = frac(L[0], L[0])
        L_frac.append(new_frac)
        return L_frac
    for i in range(len(L)):
        for j in range(len(L)):
            if L[j] != 0 and L[i] <= L[j]:
                new_frac = frac(L[i], L[j])
                exists = 0
                for elem in L_frac:
                    if elem == new_frac:
                        exists = 1
                        break
                if exists == 0:
                    L_frac.append(new_frac)
    L_frac.sort()
    return L_frac


def same_f(fa, fb):
    return abs(fa - fb) < delta


if __name__ == "__main__":
    L = [0, 7, 11, 8, 10, 18]
    print(f"L = {L}")
    fractions = list_frac(L)
    print(f"Fraction are: {L_frac}")
    L_half = []
    min_diff = 100.0  # starts with an arbitary large float
    for elem in fractions:
        if same_f(elem.minus_half, min_diff):
            L_half.append(elem)
        else:
            if elem.minus_half < min_diff:
                min_diff = elem.minus_half
                L_half.clear()
                L_half.append(elem)
    print(f"Closet to 1/2 is: {L_half}")
