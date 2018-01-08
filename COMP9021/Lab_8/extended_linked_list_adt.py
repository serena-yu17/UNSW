# Written by Eric Martin for COMP9021


'''
A Linked List abstract data type
'''

from copy import deepcopy


class Node:
    def __init__(self, value=None):
        self.value = value
        self.next_node = None


class LinkedList:
    def __init__(self, L=None, key=lambda x: x):
        self.key = key
        if L is None:
            self.head = None
            return
        # If L is not subscriptable, then will generate an exception that reads:
        # TypeError: 'type_of_L' object is not subscriptable
        if not len(L[: 1]):
            self.head = None
            return
        node = Node(L[0])
        self.head = node
        for e in L[1:]:
            node.next_node = Node(e)
            node = node.next_node

    def print(self, separator=', '):
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
        print(separator.join(nodes))

    def duplicate(self):
        if not self.head:
            return
        node = self.head
        node_copy = Node(deepcopy(node.value))
        L = LinkedList(key=self.key)
        L.head = node_copy
        node = node.next_node
        while node:
            node_copy.next_node = Node(deepcopy(node.value))
            node_copy = node_copy.next_node
            node = node.next_node
        return L

    def __len__(self):
        length = 0
        node = self.head
        while node:
            length += 1
            node = node.next_node
        return length

    def apply_function(self, function):
        node = self.head
        while node:
            node.value = function(node.value)
            node = node.next_node

    def is_sorted(self):
        node = self.head
        while node and node.next_node:
            if self.key(node.value) > self.key(node.next_node.value):
                return False
            node = node.next_node
        return True

    def extend(self, L):
        if not L.head:
            return
        if not self.head:
            self.head = L.head
            return
        node = self.head
        while node.next_node:
            node = node.next_node
        node.next_node = L.head

    def reverse(self):
        if not self.head:
            return
        node = self.head.next_node
        self.head.next_node = None
        while node:
            next_node = node.next_node
            node.next_node = self.head
            self.head = node
            node = next_node

    def recursive_reverse(self):
        if not self.head or not self.head.next_node:
            return
        node = self.head
        while node.next_node.next_node:
            node = node.next_node
        last_node = node.next_node
        node.next_node = None
        self.recursive_reverse()
        last_node.next_node = self.head
        self.head = last_node

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
        if not self.head:
            self.head = Node(value)
            return
        head = self.head
        self.head = Node(value)
        self.head.next_node = head

    def append(self, value):
        if not self.head:
            self.head = Node(value)
            return
        node = self.head
        while node.next_node:
            node = node.next_node
        node.next_node = Node(value)

    def insert_value_at(self, value, index):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            return
        if index <= 0:
            new_node.next_node = self.head
            self.head = new_node
            return
        node = self.head
        while node.next_node and index > 1:
            node = node.next_node
            index -= 1
        next_node = node.next_node
        node.next_node = new_node
        new_node.next_node = next_node

    def insert_value_before(self, value_1, value_2):
        if not self.head:
            return False
        if self.head.value == value_2:
            self.insert_value_at(value_1, 0)
            return True
        node = self.head
        while node.next_node and node.next_node.value != value_2:
            node = node.next_node
        if not node.next_node:
            return False
        new_node = Node(value_1)
        new_node.next_node = node.next_node
        node.next_node = new_node
        return True

    def insert_value_after(self, value_1, value_2):
        if not self.head:
            return False
        node = self.head
        while node and node.value != value_2:
            node = node.next_node
        if not node:
            return False
        new_node = Node(value_1)
        new_node.next_node = node.next_node
        node.next_node = new_node
        return True

    def insert_sorted_value(self, value):
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
        node.next_node = new_node

    def delete_value(self, value):
        if not self.head:
            return False
        if self.head.value == value:
            self.head = self.head.next_node
            return True
        node = self.head
        while node.next_node and node.next_node.value != value:
            node = node.next_node
        if node.next_node:
            node.next_node = node.next_node.next_node
            return True
        return False

    def remove_duplicates(self):
        '''
        >>> LL = LinkedList([1, 1, 1, 2, 1, 2, 1, 2, 3, 3, 2, 1])
        >>> LL.remove_duplicates()
        >>> LL.print()
        1, 2, 3
        '''
        if not self.head:
            return
        if not self.head.next_node:
            return
        front = self.head
        while front:
            p_seek = front
            while p_seek and p_seek.next_node:
                if p_seek.next_node.value == front.value:
                    nxt = p_seek.next_node.next_node
                    p_seek.next_node.next_node = None
                    p_seek.next_node = nxt
                else:
                    p_seek = p_seek.next_node
            front = front.next_node


if __name__ == '__main__':
    import doctest

    doctest.testmod()
