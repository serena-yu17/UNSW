from copy import deepcopy


class Node:
    def __init__(self, value=None):
        self.value = value
        self.next_node = None
        self.previous_node = None


class LinkedList:
    def __init__(self, L=None, key=lambda x: x):
        self.key = key
        if L is None:
            self.head = None
            self.length = 0
            return
        if not len(L[: 1]):
            self.head = None
            self.length = 0
            return
        self.head = Node(L[0])
        front = self.head
        for i in range(1, len(L)):
            new_node = Node(L[i])
            front.next_node = new_node
            new_node.previous_node = front
            front = new_node
        self.length = len(L)

    def print(self, sep=', '):
        if not self.head:
            return
        nodes = []
        node = self.head
        while node:
            nodes.append(str(node.value))
            node = node.next_node
            if len(nodes) > 1000:
                print("LL print: output too long")
                return
        print(sep.join(nodes))

    def duplicate(self):
        if not self.head:
            return
        node = self.head
        node_L = Node(deepcopy(node.value))
        L = DoubleLinkedList(key=self.key)
        L.head = node_L
        node = node.next_node
        while node:
            new_node = Node(deepcopy(node.value))
            node_L.next_node = new_node
            new_node.previous_node = node_L
            node_L = node_L.next_node
            node = node.next_node
        L.length = self.length
        return L

    def __len__(self):
        return self.length

    def apply_function(self, function):
        node = self.head
        while node:
            node.value = function(node.value)
            node = node.next_node

    def is_sorted(self):
        node = self.head
        if node:
            while node.next_node:
                if self.key(node.value) > self.key(node.next_node.value):
                    return False
                node = node.next_node
        return True

    def extend(self, L):
        if not L.head:
            return
        self.length += len(L)
        if not self.head:
            self.head = L.head
            return
        node = self.head
        while node.next_node:
            node = node.next_node
        node.next_node = L.head

    def reverse(self):
        '''
        >>> L = LinkedList([1,2,3,4,5,6,7])
        >>> L.reverse()
        >>> L.print()
        7, 6, 5, 4, 3, 2, 1
        '''
        if self.head:
            node = self.head
            while node:
                nxt = node.next_node
                last = node.previous_node
                node.next_node = last
                node.previous_node = nxt
                if not nxt:
                    break
                node = nxt
            self.head = node

    def index_of_value(self, value):
        index = 0
        node = self.head
        while node:
            if node.value == value:
                return index
            index += 1
            node = node.next_node
        return -1

    def value_at(self, index):
        if index < 0:
            return
        node = self.head
        while node and index:
            node = node.next_node
            index -= 1
        if node:
            return node.value
        return

    def prepend(self, value):
        self.length += 1
        if not self.head:
            self.head = Node(value)
            return
        head = self.head
        self.head = Node(value)
        self.head.next_node = head
        head.previous_node = self.head

    def append(self, value):
        self.length += 1
        if not self.head:
            self.head = Node(value)
            return
        node = self.head
        while node.next_node:
            node = node.next_node
        new_node = Node(value)
        node.next_node = new_node
        new_node.previous_node = node

    def insert_value_at(self, value, index):
        self.length += 1
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            return
        if index <= 0:
            new_node.next_node = self.head
            self.head.previous_node = new_node
            self.head = new_node
            return
        node = self.head
        while node.next_node and index > 1:
            node = node.next_node
            index -= 1
        nxt = node.next_node
        node.next_node = new_node
        new_node.previous_node = node
        new_node.next_node = nxt
        nxt.previous_node = new_node

    def insert_value_before(self, value_1, value_2):
        if not self.head:
            return False
        self.length += 1
        if self.head.value == value_2:
            self.insert_value_at(value_1, 0)
            return True
        node = self.head
        while node.next_node.value != value_2:
            if not node.next_node:
                return False
            node = node.next_node
        new_node = Node(value_1)
        new_node.next_node = node.next_node
        node.next_node.previous_node = new_node
        node.next_node = new_node
        return True

    def insert_value_after(self, value_1, value_2):
        if not self.head:
            return False
        self.length += 1
        node = self.head
        while node and node.value != value_2:
            node = node.next_node
        if not node:
            return False
        new_node = Node(value_1)
        new_node.next_node = node.next_node
        node.next_node.previous_node = new_node
        node.next_node = new_node
        return True

    def insert_sorted_value(self, value):
        self.length += 1
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            return
        if value <= self.key(self.head.value):
            new_node.next_node = self.head
            self.head = new_node
            return
        node = self.head
        while node.next_node and value > self.key(node.next_node.value):
            node = node.next_node
        new_node.next_node = node.next_node
        node.next_node.previous_node = new_node
        node.next_node = new_node

    def delete_value(self, value):
        if not self.head:
            return False
        if self.head.value == value:
            self.head = self.head.next_node
            self.length -= 1
            return True
        node = self.head
        while node.next_node and node.next_node.value != value:
            node = node.next_node
        if node.next_node:
            node.next_node = node.next_node.next_node
            node.next_node.previous_node = node
            self.length -= 1
            return True
        return False

if __name__ == "__main__":
    import doctest
    doctest.testmod()
