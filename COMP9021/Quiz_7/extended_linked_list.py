# Written by **** for COMP9021

from linked_list_adt import *


class ExtendedLinkedList(LinkedList):
    def __init__(self, L=None):
        super().__init__(L)

    def rearrange(self):
        if len(self) < 2:
            return
        current = self.head
        while current.next_node is not None:
            current = current.next_node
        oddhead = Node()
        evenhead = Node()
        odd = oddhead
        even = evenhead
        current = self.head
        nxt = current.next_node
        while 1:
            if current.value & 1 == 1:
                current.next_node = odd.next_node
                odd.next_node = current
                odd = current
            else:
                current.next_node = even.next_node
                even.next_node = current
                even = current
            if nxt is None:
                break
            current = nxt
            nxt = current.next_node
        if oddhead.next_node is not None:
            self.head = oddhead.next_node
            odd.next_node = evenhead.next_node
        else:
            self.head = evenhead.next_node
        # cleanup
        oddhead.next_node = None
        evenhead.next_node = None
