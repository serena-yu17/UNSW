# Written by Eric Martin for COMP9021
class EmptyPriorityQueueError(Exception):
    def __init__(self, message):
        self.message = message


class PriorityQueue():
    min_capacity = 4

    def __init__(self, capacity=min_capacity):
        self.min_capacity = capacity
        self._data = [None] * capacity
        self._length = 0
        self._elements = dict()

    def __len__(self):
        return self._length

    def is_empty(self):
        return self._length == 0

    def insert(self, tup):
        if tup[0] not in self._elements:
            if self._length + 1 == len(self._data):
                self._resize(2 * len(self._data))
            self._length += 1
            self._data[self._length] = list(tup)
            self._elements[tup[0]] = self._length
            self._bubble_up(self._length)
        else:
            pos = self._elements[tup[0]]
            self._data[pos][1] = tup[1]
            if pos!=1 and tup[1] > self._data[pos // 2][1]:
                self._bubble_up(pos)
            elif (pos * 2 < self._length and tup[1] < self._data[pos * 2][1]) or (
                            pos * 2 + 1 < self._length and tup[1] < self._data[pos * 2 + 1][1]):
                self._bubble_down(pos)

    def delete(self):
        if self.is_empty():
            raise EmptyPriorityQueueError('Cannot delete element from empty priority queue')
        max_element = self._data[1][0]
        self._elements[self._data[1][0]], self._elements[self._data[self._length][0]] = \
            self._elements[self._data[self._length][0]], self._elements[self._data[1][0]]
        self._data[1], self._data[self._length] = self._data[self._length], self._data[1]
        self._length -= 1
        # When the priority queue is one quarter full, we reduce its size to make it half full,
        # provided that it would not reduce its capacity to less than the minimum required.
        if self.min_capacity // 2 <= self._length <= len(self._data) // 4:
            self._resize(len(self._data) // 2)
        self._bubble_down(1)
        return max_element

    def _bubble_up(self, i):
        if i > 1 and self._data[i][1] > self._data[i // 2][1]:
            self._elements[self._data[i // 2][0]], self._elements[self._data[i][0]] = \
                self._elements[self._data[i][0]], self._elements[self._data[i // 2][0]]
            self._data[i // 2], self._data[i] = self._data[i], self._data[i // 2]
            self._bubble_up(i // 2)

    def _bubble_down(self, i):
        child = 2 * i
        if child < self._length and self._data[child + 1][1] > self._data[child][1]:
            child += 1
        if child <= self._length and self._data[i][1] < self._data[child][1]:
            self._elements[self._data[child][0]], self._elements[self._data[i][0]] = \
                self._elements[self._data[i][0]], self._elements[self._data[child][0]]
            self._data[child], self._data[i] = self._data[i], self._data[child]
            self._bubble_down(child)

    def _resize(self, new_size):
        self._data = list(self._data[: self._length + 1]) + [None] * (new_size - self._length - 1)


if __name__ == '__main__':
    pq = PriorityQueue()
    L = [('A', 13), ('B', 13), ('C', 4), ('D', 15), ('E', 9), ('F', 4), ('G', 5), \
         ('H', 14), ('A', 4), ('B', 11), ('C', 15), ('D', 2), ('E', 17), ('A', 8), \
         ('B', 14), ('C', 12), ('D', 9), ('E', 5), ('A', 6), ('B', 16)]
    for e in L:
        pq.insert(e)
        print(f'{pq._data[: len(pq) + 1]}    {len(pq._data)}')
    for _ in range(len(pq)):
        print(f'{pq.delete()}   {pq._data[: len(pq) + 1]}        {len(pq._data)}')
