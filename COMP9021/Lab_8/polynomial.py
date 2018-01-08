from collections import defaultdict


def isOP(ch):
    if ch == '+' or ch == '-':
        return 1
    return 0


# number  x  ^ num
def parse(s):
    poly = defaultdict(int)
    s = s.strip()
    if s[0] == '+':
        return None
    if s[0] == '-' and s[1] == '0':
        return None
    if not isOP(s[0]):
        s = "+" + s
    i = 0
    while i < len(s):
        coef = None
        pow = 0
        pos = 1
        if isOP(s[i]):
            if s[i] == '-':
                pos = -1
        else:
            return None
        i += 1

        while i < len(s) and s[i] == ' ':
            i += 1

        if not s[i].isdigit() and s[i] != 'x':
            return None

        while i < len(s) and s[i].isdigit():
            if coef is None:
                coef = int(s[i])
            else:
                coef *= 10
                coef += int(s[i])
            i += 1

        if pos == -1 and coef:
            coef = -coef

        while i < len(s) and s[i] == ' ':
            i += 1

        if i == len(s):
            poly[pow] += coef
            break

        if s[i] == 'x':
            i += 1
            pow = 1

            if coef is None:
                coef = pos

            if i == len(s):
                poly[pow] += coef
                break

            while i < len(s) and s[i] == ' ':
                i += 1

            if i == len(s):
                poly[pow] += coef
                break

            if s[i] == '^':
                pow = 0
                i += 1

                if i == len(s):
                    poly[pow] += coef
                    break

                while i < len(s) and s[i] == ' ':
                    i += 1

                if i == len(s):
                    poly[pow] += coef
                    break

                if not s[i].isdigit():
                    return None

                while i < len(s) and s[i].isdigit():
                    pow *= 10
                    pow += int(s[i])
                    i += 1

                if i == len(s):
                    poly[pow] += coef
                    break

        while i < len(s) and s[i] == ' ':
            i += 1

        poly[pow] += coef
        if i == len(s):
            break
    return poly


def constructLL(poly):
    head = Monomial()
    if not poly:
        return None
    front = head
    for pow in sorted(poly, reverse=True):
        new_node = Monomial(poly[pow], pow)
        front.next_monomial = new_node
        front = front.next_monomial
    return head.next_monomial


class Monomial:
    def __init__(self, coefficient=0, degree=0):
        self.coefficient = coefficient
        self.degree = degree
        self.next_monomial = None


class Polynomial:
    def __init__(self, s):
        self.head = constructLL(parse(s))
        if not self.head:
            print("Incorrect input")

    def __repr__(self):
        out = []
        front = self.head
        while front:
            if front.coefficient == 0 and not front.next_monomial:
                out.append('0')
            else:
                if front.degree != 0:
                    if front.coefficient < 0:
                        if len(out) == 0:
                            out.append('-')
                        else:
                            out.append(' - ')
                    else:
                        if len(out) != 0:
                            out.append(' + ')
                    if abs(front.coefficient) != 1:
                        out.append(str(abs(front.coefficient)))
                    out.append('x')
                    if front.degree != 1:
                        out.append('^')
                        out.append(str(front.degree))
                else:
                    if front.coefficient > 0:
                        out.append(' + ')
                    out.append(str(front.coefficient))
            front = front.next_monomial
        return "".join(out)


poly_0 = Polynomial('-2x + 7x^3 +x - 0 + 2 -x^3 + x^23 - 12x^8 + 45 x ^ 6 -x^47')
print(poly_0)
