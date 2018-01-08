class EvalException(Exception):
    def __init__(self, msg):
        self.message = msg


def calc(opr1, opr2, op):
    if op == '+':
        return opr1 + opr2
    if op == '-':
        return opr1 - opr2
    if op == '*':
        return opr1 * opr2
    if op == '/':
        if opr2 == 0:
            raise EvalException("Division by 0")
        return opr1 / opr2

def evaluate(expr):
    pair = {')':'(', ']':'[', '}':'{'}
    opening = set()
    closing = set()
    for key in pair:
        closing.add(key)
        opening.add(pair[key])
    operators = {'+', '-', '*', '/'}
    stack = list()
    i = 0
    while i < len(expr):
        num = 0
        found = 0
        while i < len(expr) and expr[i].isdigit():
            num *= 10
            num += int(expr[i])
            i+=1
            found = 1
        if found:
            stack.append(num)
            continue
        if expr[i] in opening:
            stack.append(expr[i])
            i += 1
            continue
        if expr[i] in closing:
            if len(stack) < 3:
                raise EvalException("Parentheses missing")
            opr2 = stack.pop()
            op = stack.pop()
            opr1 = stack.pop()
            if stack[-1] != pair[expr[i]]:
                raise EvalException("Parentheses not paired")
            stack.pop()
            stack.append(calc(opr1, opr2, op))
            i += 1
            continue
        if expr[i] in operators:
            stack.append(expr[i])
        i += 1
    print(stack[0])
            
            
        
