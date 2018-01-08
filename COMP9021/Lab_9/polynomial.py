import sys


def isOP(ch):
    if ch == '+' or ch == '-':
        return 1
    return 0


def insert_monomial(head, pow, coef):
    if coef == 0:
        return
    front = head
    while front.next_monomial and front.next_monomial.degree > pow:
        front = front.next_monomial
    if not front.next_monomial:
        front.next_monomial = Monomial(coef, pow)
    elif front.next_monomial.degree == pow:
        front.next_monomial.coefficient += coef
    else:
        temp = front.next_monomial
        front.next_monomial = Monomial(coef, pow)
        front.next_monomial.next_monomial = temp


# number  x  ^ num
def parse(s):
    head = Monomial()
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
            insert_monomial(head, pow, coef)
            break

        if s[i] == 'x':
            i += 1
            pow = 1

            if coef is None:
                coef = pos

            if i == len(s):
                insert_monomial(head, pow, coef)
                break

            while i < len(s) and s[i] == ' ':
                i += 1

            if i == len(s):
                insert_monomial(head, pow, coef)
                break

            if s[i] == '^':
                pow = 0
                i += 1

                if i == len(s):
                    insert_monomial(head, pow, coef)
                    break

                while i < len(s) and s[i] == ' ':
                    i += 1

                if i == len(s):
                    insert_monomial(head, pow, coef)
                    break

                if not s[i].isdigit():
                    return None

                while i < len(s) and s[i].isdigit():
                    pow *= 10
                    pow += int(s[i])
                    i += 1

                if i == len(s):
                    insert_monomial(head, pow, coef)
                    break

        while i < len(s) and s[i] == ' ':
            i += 1

        insert_monomial(head, pow, coef)
        if i == len(s):
            break
    return head.next_monomial


class Monomial:
    def __init__(self, coefficient=0, degree=0):
        self.coefficient = coefficient
        self.degree = degree
        self.next_monomial = None

    def copy(self):
        out = Monomial()
        out.coefficient = self.coefficient
        out.degree = self.degree
        return out


class Polynomial:
    def __init__(self, s=None):
        if s:
            self.head = parse(s)
            if not self.head:
                print("Incorrect input")
        else:
            self.head = Monomial()

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
                    if front.coefficient > 0 and len(out):
                        out.append(' + ')
                    out.append(str(front.coefficient))
            front = front.next_monomial
        if not len(out):
            out = ['0']
        return "".join(out)

    def __add__(self, other):
        front1 = self.head
        front2 = other.head
        if not front1:
            return front2
        if not front2:
            return front1
        head = Monomial()
        result = head
        while front1 and front2:
            if front1.degree > front2.degree:
                result.next_monomial = front1.copy()
                result = result.next_monomial
                front1 = front1.next_monomial
            elif front1.degree == front2.degree:
                if front1.coefficient + front2.coefficient != 0:
                    new_node = Monomial(front1.coefficient + front2.coefficient, front1.degree)
                    result.next_monomial = new_node
                    result = result.next_monomial
                    front1 = front1.next_monomial
                    front2 = front2.next_monomial
            elif front2.degree > front1.degree:
                result.next_monomial = front2.copy()
                result = result.next_monomial
                front2 = front1.next_monomial
        while front1:
            result.next_monomial = front1.copy()
            result = result.next_monomial
            front1 = front1.next_monomial
        while front2:
            result.next_monomial = front2.copy()
            result = result.next_monomial
            front2 = front2.next_monomial
        out = Polynomial()
        out.head = head.next_monomial
        head.next_monomial = None
        return out

    def __sub__(self, other):
        front1 = self.head
        front2 = other.head
        head = Monomial()
        result = head
        while front1 and front2:
            if front1.degree > front2.degree:
                result.next_monomial = front1.copy()
                result = result.next_monomial
                front1 = front1.next_monomial
            elif front1.degree == front2.degree:
                if front1.coefficient - front2.coefficient != 0:
                    new_node = Monomial(front1.coefficient - front2.coefficient, front1.degree)
                    result.next_monomial = new_node
                    result = result.next_monomial
                front1 = front1.next_monomial
                front2 = front2.next_monomial
            elif front2.degree > front1.degree:
                result.next_monomial = front2.copy()
                result = result.next_monomial
                front2 = front1.next_monomial
        while front1:
            result.next_monomial = front1.copy()
            result = result.next_monomial
            front1 = front1.next_monomial
        while front2:
            result.next_monomial = front2.copy()
            result = result.next_monomial
            result.coefficient = - result.coefficient
            front2 = front2.next_monomial
        out = Polynomial()
        out.head = head.next_monomial
        head.next_monomial = None
        return out

    def __mul__(self, other):
        front1 = self.head
        front2 = other.head
        if not front1 or not front2:
            return Polynomial()
        head = Monomial()
        while front1:
            front2 = other.head
            while front2:
                if front1.coefficient and front2.coefficient:
                    insert_monomial(head, front1.degree + front2.degree, front1.coefficient * front2.coefficient)
                front2 = front2.next_monomial
            front1 = front1.next_monomial
        out = Polynomial()
        out.head = head.next_monomial
        head.next_monomial=None
        return out

    def __truediv__(self, other):
        if not other.head:
            sys.exit()
        if not self.head:
            return Polynomial()
        out = Polynomial()
        head = out.head
        front1 = head
        front_self = self.head
        while front_self:
            front1.next_monomial = Monomial(front_self.coefficient, front_self.degree)
            front1 = front1.next_monomial
            front_self = front_self.next_monomial
        front1=head.next_monomial
        head.next_monomial=None
        head=front1
        ratio = Polynomial()
        while head and head.degree >= other.head.degree:
            rat = Polynomial()
            rat.head = Monomial(int(head.coefficient / other.head.coefficient), head.degree - other.head.degree)
            out = out - (other * rat)
            head=out.head
            ratio = ratio + rat
        return ratio


poly_10 = Polynomial('-11x^4 + 3x^2 + 7x + 9')
poly_11 = Polynomial('5x^2 -8x - 6')
poly_12 = poly_10 * poly_11
print(poly_12)
print(poly_12/poly_10)