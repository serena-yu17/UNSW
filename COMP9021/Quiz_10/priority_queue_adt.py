# Written by Eric Martin for COMP9021


'''
A priority queue abstract data type.
'''


class EmptyPriorityQueueError(Exception):
    def __init__(self, message):
        self.message = message

    
class PriorityQueue():
    min_capacity = 10

    def __init__(self, capacity = min_capacity):
        self.min_capacity = capacity
        self._data = [None] * capacity
        self._length = 0
        
    def __len__(self):
        '''
        >>> len(PriorityQueue(100))
        0
        '''
        return self._length

    def is_empty(self):
        return self._length == 0

    def insert(self, element):
        '''
        >>> pq = PriorityQueue(4)
        >>> L = [13, 13, 4, 15, 9, 4, 5, 14, 4, 11, 15, 2, 17, 8, 14, 12, 9, 5, 6, 16]
        >>> for e in L: pq.insert(e); print(f'{pq._data[: len(pq) + 1]}    {len(pq._data)}')
        [None, 13]    4
        [None, 13, 13]    4
        [None, 13, 13, 4]    4
        [None, 15, 13, 4, 13]    8
        [None, 15, 13, 4, 13, 9]    8
        [None, 15, 13, 4, 13, 9, 4]    8
        [None, 15, 13, 5, 13, 9, 4, 4]    8
        [None, 15, 14, 5, 13, 9, 4, 4, 13]    16
        [None, 15, 14, 5, 13, 9, 4, 4, 13, 4]    16
        [None, 15, 14, 5, 13, 11, 4, 4, 13, 4, 9]    16
        [None, 15, 15, 5, 13, 14, 4, 4, 13, 4, 9, 11]    16
        [None, 15, 15, 5, 13, 14, 4, 4, 13, 4, 9, 11, 2]    16
        [None, 17, 15, 15, 13, 14, 5, 4, 13, 4, 9, 11, 2, 4]    16
        [None, 17, 15, 15, 13, 14, 5, 8, 13, 4, 9, 11, 2, 4, 4]    16
        [None, 17, 15, 15, 13, 14, 5, 14, 13, 4, 9, 11, 2, 4, 4, 8]    16
        [None, 17, 15, 15, 13, 14, 5, 14, 13, 4, 9, 11, 2, 4, 4, 8, 12]    32
        [None, 17, 15, 15, 13, 14, 5, 14, 13, 4, 9, 11, 2, 4, 4, 8, 12, 9]    32
        [None, 17, 15, 15, 13, 14, 5, 14, 13, 5, 9, 11, 2, 4, 4, 8, 12, 9, 4]    32
        [None, 17, 15, 15, 13, 14, 5, 14, 13, 6, 9, 11, 2, 4, 4, 8, 12, 9, 4, 5]    32
        [None, 17, 16, 15, 13, 15, 5, 14, 13, 6, 14, 11, 2, 4, 4, 8, 12, 9, 4, 5, 9]    32
        '''
        if self._length + 1 == len(self._data):
            self._resize(2 * len(self._data))
        self._length += 1
        self._data[self._length] = element
        self._bubble_up(self._length)

    def delete(self):
        '''
        >>> pq = PriorityQueue(4)
        >>> L = [13, 13, 4, 15, 9, 4, 5, 14, 4, 11, 15, 2, 17, 8, 14, 12, 9, 5, 6, 16]
        >>> for e in L: pq.insert(e)
        >>> for _ in range(len(L)):
        ...     print(f'{pq.delete():2d} {pq._data[: len(pq) + 1]}    {len(pq._data)}')
        17 [None, 16, 15, 15, 13, 14, 5, 14, 13, 6, 9, 11, 2, 4, 4, 8, 12, 9, 4, 5]    32
        16 [None, 15, 14, 15, 13, 11, 5, 14, 13, 6, 9, 5, 2, 4, 4, 8, 12, 9, 4]    32
        15 [None, 15, 14, 14, 13, 11, 5, 8, 13, 6, 9, 5, 2, 4, 4, 4, 12, 9]    32
        15 [None, 14, 13, 14, 13, 11, 5, 8, 12, 6, 9, 5, 2, 4, 4, 4, 9]    32
        14 [None, 14, 13, 9, 13, 11, 5, 8, 12, 6, 9, 5, 2, 4, 4, 4]    32
        14 [None, 13, 13, 9, 12, 11, 5, 8, 4, 6, 9, 5, 2, 4, 4]    32
        13 [None, 13, 12, 9, 6, 11, 5, 8, 4, 4, 9, 5, 2, 4]    32
        13 [None, 12, 11, 9, 6, 9, 5, 8, 4, 4, 4, 5, 2]    32
        12 [None, 11, 9, 9, 6, 5, 5, 8, 4, 4, 4, 2]    32
        11 [None, 9, 6, 9, 4, 5, 5, 8, 2, 4, 4]    32
         9 [None, 9, 6, 8, 4, 5, 5, 4, 2, 4]    32
         9 [None, 8, 6, 5, 4, 5, 4, 4, 2]    16
         8 [None, 6, 5, 5, 4, 2, 4, 4]    16
         6 [None, 5, 4, 5, 4, 2, 4]    16
         5 [None, 5, 4, 4, 4, 2]    16
         5 [None, 4, 4, 4, 2]    8
         4 [None, 4, 2, 4]    8
         4 [None, 4, 2]    4
         4 [None, 2]    4
         2 [None]    4
        >>> pq.delete()
        Traceback (most recent call last):
        ...
        EmptyPriorityQueueError: Cannot delete element from empty priority queue
        '''
        if self.is_empty():
            raise EmptyPriorityQueueError('Cannot delete element from empty priority queue')
        max_element = self._data[1]
        self._data[1], self._data[self._length] = self._data[self._length], self._data[1]
        self._length -= 1
        # When the priority queue is one quarter full, we reduce its size to make it half full,
        # provided that it would not reduce its capacity to less than the minimum required.
        if self.min_capacity // 2 <= self._length <= len(self._data) // 4:
            self._resize(len(self._data) // 2)
        self._bubble_down(1)
        return max_element
        
    def _bubble_up(self, i):
        if i > 1 and self._data[i] > self._data[i // 2]:
            self._data[i // 2], self._data[i] = self._data[i], self._data[i // 2]
            self._bubble_up(i // 2)

    def _bubble_down(self, i):
        child = 2 * i
        if child < self._length and self._data[child + 1] > self._data[child]:
            child += 1
        if child <= self._length and self._data[i] < self._data[child]:
            self._data[child], self._data[i] = self._data[i], self._data[child]
            self._bubble_down(child)

    def _resize(self, new_size):
        self._data = list(self._data[: self._length + 1]) + [None] * (new_size - self._length - 1)


if __name__ == '__main__':
    import doctest
    doctest.testmod()    
