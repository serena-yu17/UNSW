import sys

op = {'+', '-', '*', '/'}
open_paren = {'(': 0, '[': 1, '{': 2}
close_paren = {')': 0, ']': 1, '}': 2}
priority = {'+': 1, '-': 1, '*': 2, '/': 2, '(': 100, ')': 100}


def preprocess(exp):
    paren = list()
    result = list()
    last = ""
    i = 0
    ub = len(exp)
    surrounded = 0
    while exp[i] in open_paren and exp[ub - 1] in close_paren and open_paren[exp[i]] == close_paren[exp[ub - 1]]:
        i += 1
        ub -= 1
        surrounded = 1
    while i < ub:
        if exp[i] in op and result[-1] in op:
            sys.exit(1)  # consective op
        if last == ' ' and exp[i].isdigit() and result[-1].isdigit():
            sys.exit(1)  # 2 numbers connected by only space(s)

        if exp[i].isdigit() or exp[i] in op:
            result.append((exp[i]))
        elif exp[i] in open_paren:
            result.append('(')
            paren.append(exp[i])
        elif exp[i] in close_paren:
            result.append(')')
            if not len(paren) or open_paren[paren[-1]] != close_paren[exp[i]]:
                sys.exit(1)
            else:
                paren.pop()
        else:
            if exp[i] != ' ':
                sys.exit(1)
        last = exp[i]
        i += 1
    if len(paren):
        sys.exit(1)
    if not surrounded and len(result) > 1:
        sys.exit(1)
    return result


def parse(exp):
    revPolish = list()
    stack = list()
    i = 0
    while i < len(exp):
        neg = 0
        if i < len(exp) - 1 and exp[i] == '-' and (i == 0 or exp[i - 1] == '(') and exp[i + 1].isdigit():
            neg = 1
            revPolish.append(0)
            i += 1
        buffer = 0
        isNum = 0
        while i < len(exp) and exp[i].isdigit():
            buffer *= 10
            buffer += ord(exp[i]) - ord('0')
            isNum = 1
            i += 1
        if isNum:
            revPolish.append(buffer)
        if neg:
            revPolish.append('-')
        if i < len(exp) and (exp[i] in op or exp[i] == '(' or exp[i] == ')'):
            if exp[i] == ')':
                while len(stack) and stack[-1] != '(':
                    revPolish.append(stack.pop())
                if not len(stack):
                    sys.exit(1)  # parentheses not paired
                stack.pop()
                i += 1
            while len(stack) and stack[-1] != '(' and (i == len(exp) or priority[exp[i]] <= priority[stack[-1]]):
                revPolish.append(stack.pop())
            if i < len(exp) and exp[i] != ')':
                stack.append(exp[i])
                i += 1
    while len(stack):
        if stack[-1] == '(':
            sys.exit(1)  # parentheses not paired
        revPolish.append(stack.pop())
    return revPolish


def calc(opr1, ope, opr2):
    if ope == '+':
        return opr1 + opr2
    if ope == '-':
        return opr1 - opr2
    if ope == '*':
        return opr1 * opr2
    if ope == '/':
        if opr2 == 0:
            sys.exit(1)  # divisor cannot be 0
        return opr1 / opr2


def calcRevPolish(revPolish):
    stack = list()
    i = 0
    while i < len(revPolish):
        if isinstance(revPolish[i], int):
            stack.append(revPolish[i])
            i += 1
        if len(stack) < 2 and i < len(revPolish) and revPolish[i] in op:
            sys.exit(1)  # operators and operands are not paired
        if i < len(revPolish) and revPolish[i] in op:
            opr2 = stack.pop()
            opr1 = stack.pop()
            stack.append(calc(opr1, revPolish[i], opr2))
            i += 1
    return stack[-1]


def evaluate(exp):
    exp = preprocess(exp)
    revPolish = parse(exp)
    return calcRevPolish(revPolish)


if __name__ == "__main__":
    exp = input("expression: ")
    print(evaluate(exp))
