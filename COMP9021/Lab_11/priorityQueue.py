class EmptyPriorityQueueError(Exception):
    def __init__(self, message):
        self.message = message

class PriorityQueue:
    min_capacity = 4

    def __init__(self, capacity=min_capacity):
        self.capacity = capacity
        self.array = [None] * self.capacity
        self.size = 0
        self.elements = dict()

    def __len__(self):
        return self.size

    def expand(self):
        if self.size >= self.capacity >> 1:
            self.capacity <<=1
            newArr = [None] * self.capacity
            for i in range(self.size + 1):
                newArr[i] = self.array[i]
            self.array = newArr

    def shrink(self):
        if self.size < (self.capacity >> 2):
            self.capacity >>= 1
            newArr= [None] * self.capacity
            for i in range(self.size + 1):
                newArr[i] = self.array[i]
            self.array = newArr

    def bubble_up(self, index):        
        while index > 1:
            parentId = index >> 1
            if self.array[index][1] > self.array[parentId][1]:
                self.elements[self.array[index][0]], self.elements[self.array[parentId][0]] = self.elements[
                    self.array[parentId][0]], self.elements[self.array[index][0]]
                self.array[index],self.array[parentId] = self.array[parentId],self.array[index]
                index = parentId
            else:
                return            

    def bubble_down(self, index):
        while index <<1 <= self.size + 1:
            child = index << 1
            if child < self.size and self.array[child][1] < self.array[child + 1][1]:
                child += 1
            if child < self.size + 1 and self.array[index][1] < self.array[child][1]:
                self.elements[self.array[index][0]], self.elements[self.array[child][0]] = self.elements[
                    self.array[child][0]], self.elements[self.array[index][0]]
                self.array[index],self.array[child] = self.array[child],self.array[index]
                index = child
            else:
                return  

    def insert(self, tup):
        if tup[0] not in self.elements:
            if self.size + 1 == self.capacity:
                self.expand()
            self.array[self.size + 1] = list(tup)
            self.size += 1
            self.elements[tup[0]] = self.size
            self.bubble_up(self.size)
        else:
            n = self.elements[tup[0]]
            if tup[1] > self.array[n][1]:
                self.array[n][1] = tup[1]
                self.bubble_up(n)
            elif tup[1] < self.array[n][1]:                
                self.array[n][1] = tup[1]
                self.bubble_down(n)

    def __max__(self):
        return self.array[1]

    def delete(self):
        if self.size == 0:
            raise EmptyPriorityQueueError("Cannot delete element from an empty queue.")
            return
        elem = self.array[1][0]
        self.elements.pop(self.array[1][0])
        self.array[1] = self.array[self.size]
        self.elements[self.array[1][0]] = 1        
        self.size -= 1
        if self.size + 1 < self.capacity >> 2:
            self.shrink()
        self.bubble_down(1)
        return elem

if __name__ == '__main__':
    pq = PriorityQueue()
    L = [('A', 13), ('B', 13), ('C', 4), ('D', 15), ('E', 9), ('F', 4), ('G', 5), \
         ('H', 14), ('A', 4), ('B', 11), ('C', 15), ('D', 2), ('E', 17), ('A', 8), \
         ('B', 14), ('C', 12), ('D', 9), ('E', 5), ('A', 6), ('B', 16)]
    for e in L:
        pq.insert(e)
        print(f'{pq.array[: len(pq) + 1]}    {len(pq.array)}')
    print("-----------")
    for _ in range(len(pq)):
        print(f'{pq.delete()}   {pq.array[: len(pq) + 1]}        {len(pq.array)}')    

    
        
        






























        

    









        
        
