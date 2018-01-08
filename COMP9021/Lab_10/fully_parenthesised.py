import sys


class Node:
    def __init__(self, val=None):
        self.left = None
        self.right = None
        self.val = val

    def print_binary_tree(self):
        if self.val is None:
            return
        self._print_binary_tree(0, self.height())

    def _print_binary_tree(self, n, height):
        if n > height:
            return
        if not self or self.val is None:
            print('\n' * (2 ** (height - n + 1) - 1), end='')
        else:
            if self.left:
                self.left._print_binary_tree(n + 1, height)
            print('      ' * n, self.val, sep='')
            if self.right:
                self.right._print_binary_tree(n + 1, height)

    def height(self):
        if not self or self.val is None:
            return 0
        height_left = 0
        height_right = 0
        if self.left:
            height_left = self.left.height()
        if self.right:
            height_right = self.right.height()
        return max(height_left, height_right) + 1


class parse_tree:
    def __init__(self, exp):
        if not isinstance(exp, str):
            sys.exit(1)
        self.op = {'+', '-', '*', '/'}
        self.open_paren = {'(': 0, '[': 1, '{': 2}
        self.close_paren = {')': 0, ']': 1, '}': 2}
        self.priority = {'+': 1, '-': 1, '*': 2, '/': 2, '(': 100, ')': 100}
        self.head = Node
        self.preprocess(exp)
        self.parse()
        self.calcRevPolish()
        self.buildTree()
        pass

    @staticmethod
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

    def preprocess(self, exp):
        paren = list()
        result = list()
        last = ""
        i = 0
        ub = len(exp)
        surrounded = 0
        exp.strip()
        while i < ub:
            if exp[i] in self.op and result[-1] in self.op:
                sys.exit(1)  # consective op
            if last == ' ' and exp[i].isdigit() and result[-1].isdigit():
                sys.exit(1)  # 2 numbers connected by only space(s)

            if exp[i].isdigit() or exp[i] in self.op:
                result.append((exp[i]))
            elif exp[i] in self.open_paren:
                result.append('(')
                paren.append(exp[i])
            elif exp[i] in self.close_paren:
                result.append(')')
                if not len(paren) or self.open_paren[paren[-1]] != self.close_paren[exp[i]]:
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
        if not surrounded and len(paren) > 1:
            sys.exit(1)
        self.exp = result

    def parse(self):
        revPolish = list()
        stack = list()
        i = 0
        while i < len(self.exp):
            neg = 0
            if i < len(self.exp) - 1 and self.exp[i] == '-' and (i == 0 or self.exp[i - 1] == '(') and self.exp[
                        i + 1].isdigit():
                neg = 1
                revPolish.append(0)
                i += 1
            buffer = 0
            isNum = 0
            while i < len(self.exp) and self.exp[i].isdigit():
                buffer *= 10
                buffer += ord(self.exp[i]) - ord('0')
                isNum = 1
                i += 1
            if isNum:
                revPolish.append(buffer)
            if neg:
                revPolish.append('-')
            if i < len(self.exp) and (self.exp[i] in self.op or self.exp[i] == '(' or self.exp[i] == ')'):
                if self.exp[i] == ')':
                    while len(stack) and stack[-1] != '(':
                        revPolish.append(stack.pop())
                    if not len(stack):
                        sys.exit(1)  # parentheses not paired
                    stack.pop()
                    i += 1
                while len(stack) and stack[-1] != '(' and (
                                i == len(self.exp) or self.priority[self.exp[i]] <= self.priority[stack[-1]]):
                    revPolish.append(stack.pop())
                if i < len(self.exp) and self.exp[i] != ')':
                    stack.append(self.exp[i])
                    i += 1
        while len(stack):
            if stack[-1] == '(':
                sys.exit(1)  # parentheses not paired
            revPolish.append(stack.pop())
        self.revPolish = revPolish

    def calcRevPolish(self):
        stack = list()
        i = 0
        while i < len(self.revPolish):
            if isinstance(self.revPolish[i], int):
                stack.append(self.revPolish[i])
                i += 1
            if len(stack) < 2 and i < len(self.revPolish) and self.revPolish[i] in self.op:
                sys.exit(1)  # operators and operands are not paired
            if i < len(self.revPolish) and self.revPolish[i] in self.op:
                opr2 = stack.pop()
                opr1 = stack.pop()
                stack.append(self.calc(opr1, self.revPolish[i], opr2))
                i += 1
        self.result = stack[-1]

    def buildTree(self):
        stack = list()
        i = 0
        while i < len(self.revPolish):
            if isinstance(self.revPolish[i], int):
                stack.append(Node(self.revPolish[i]))
                i += 1
            if len(stack) < 2 and i < len(self.revPolish) and self.revPolish[i] in self.op:
                sys.exit(1)  # operators and operands are not paired
            if i < len(self.revPolish) and self.revPolish[i] in self.op:
                opr1 = stack.pop()
                opr2 = stack.pop()
                new_op = Node(self.revPolish[i])
                new_op.left = opr2
                new_op.right = opr1
                stack.append(new_op)
                i += 1
        self.head = stack[-1]

    def evaluate(self):
        return self.result

    def print_tree(self):
        self.head.print_binary_tree()


if __name__ == "__main__":
    tree = parse_tree('(1 + 20)*(30 - 400)')
    print(tree.evaluate())
    tree.print_tree()
    tree = parse_tree('20*4/5')
    print(tree.evaluate())
    tree.print_tree()
