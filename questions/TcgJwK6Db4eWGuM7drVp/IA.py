import heapq


class MedianHeap:
    def __init__(self):
        self.min_heap = []
        self.max_heap = []

    def add(self, num):
        if not self.max_heap or num <= -self.max_heap[0]:
            heapq.heappush(self.max_heap, -num)
        else:
            heapq.heappush(self.min_heap, num)

        if len(self.max_heap) > len(self.min_heap) + 1:
            heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))
        elif len(self.min_heap) > len(self.max_heap):
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))

    def pop_med(self):
        if len(self.max_heap) == len(self.min_heap):
            return -self.max_heap[0]
        else:
            return -self.max_heap[0]
