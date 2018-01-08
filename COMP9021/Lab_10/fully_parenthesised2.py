class TreeException(Exception):
    def __init__(self, msg):
        self.message = msg

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None        

class parse_tree:
    def __init__(self, expr):
        self.revPolish  = self.parse(expr)
        self.result = 0
        self.head = None
        self.process()

    def parse(self, expr):
        revPolish = list()
        op = list()
        pairs = {')':'(', ']':'[', '}':'{'}
        priority = {'+':1, '-':1, '*':2,'/':2}
        opening = set()
        for key in pairs:
            opening.add(pairs[key])
            priority[pairs[key]] = 32767
        buffer = 0
        i=0
        while i < len(expr):
            is_number = 0
            while i < len(expr) and expr[i].isdigit():
                buffer *= 10
                buffer += int(expr[i])
                i += 1
                is_number =1
            if is_number:
                revPolish.append(buffer)
                buffer = 0
                continue
            if expr[i] in opening:
                op.append(expr[i])
                i += 1
                continue
            if expr[i] in pairs:                
                while op[-1] != pairs[expr[i]]:
                    if op[-1] in pairs:
                        raise TreeException("Parentheses are not paired.")
                    revPolish.append(op.pop())
                    if len(op) == 0:
                        raise TreeException("Parentheses are not paired.")
                op.pop()
                i += 1
                continue
            if expr[i] in priority:
                while len(op) and op[-1] not in opening and priority[expr[i]] <= priority[op[-1]]:
                    revPolish.append(op.pop())
                op.append(expr[i])
                i += 1
                continue
            i += 1
        while len(op):
            if op[-1] in opening:
                raise TreeException("Parentheses are not paired.")
            revPolish.append(op.pop())
        return revPolish

    def calc(self, opr1, opr2, op):
        if op == '+':
            return opr1 + opr2
        if op == '-':
            return opr1 - opr2
        if op == '*':
            return opr1 * opr2
        if op == '/':
            return opr1 / opr2

    def process(self):
        calcStack = list()
        treeStack = list()
        for i in range(len(self.revPolish)):
            if (isinstance(self.revPolish[i], int)):
                calcStack.append(self.revPolish[i])
                treeStack.append(Node(self.revPolish[i]))
                i += 1
                continue
            if len(calcStack) < 2:
                raise TreeException("Invalid expression")
            opr2 = calcStack.pop()
            opr1 = calcStack.pop()
            res = self.calc(opr1, opr2, self.revPolish[i])
            calcStack.append(res)
            node1 = treeStack.pop()
            node2 = treeStack.pop()
            parent = Node(self.revPolish[i])
            parent.right = node1
            parent.left = node2
            treeStack.append(parent)
            i += 1
        if not len(calcStack):
            raise TreeException("Invalid expression")
        self.result = calcStack[0]
        self.head = treeStack[0]

    def evaluate(self):
        return self.result

    def height(self, node):
        if not node:
            return 0
        left_height = 0
        right_height = 0
        if node.left:
            left_height = self.height(node.left)
        if node.right:
            right_height = self.height(node.right)
        return max(left_height, right_height) + 1            

    def print_tree(self, node, n, height):
        if n > height:
            return
        if not node:
            print('\n' * (2 ** (height - n + 1) - 1), end = '')
        else:
            if node.left:
                self.print_tree(node.left, n + 1, height)
            print(' ' * (n * 6), node.val, sep = '')
            if node.right:
                self.print_tree(node.right, n + 1, height)

    def print_binary_tree(self):
        if not self.head:
            return
        height = self.height(self.head)
        self.print_tree(self.head, 0, height)
        
        
        
    

        












        

            
