import math as math
import heapq as h
import sys


def PrintBST(heap):

    m = math.floor(len(heap)/2)
    new_heap = []


    for i in range(m):
        x = h.heappop(heap)
        h.heappush(new_heap, x)

    print(h.heappop(heap))

    if len(new_heap) == 0:
        return
    if len(heap) == 0:
        PrintBST(new_heap)
    else:
        PrintBST(heap)
        PrintBST(new_heap)



if __name__ == "__main__":
    heap = []
    for line in  sys.stdin:
        h.heappush(heap, int(line))
    PrintBST(heap)
