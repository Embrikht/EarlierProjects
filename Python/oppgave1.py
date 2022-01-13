import math as math
import os, sys

class Teque():
    def __init__(self):
        self.head = None
        self.tail = None
        self.middle = None
        self.length = 0

    #Checks if teque is empty list
    def is_empty(self, node):
        if self.head == None:
            self.head = node
            self.tail = node
            self.middle = node

    def push_back(self, x):
        v = Node(x, prev=self.tail, next=None)
        self.is_empty(v)
        self.tail.next = v
        self.tail = v

        #updating length of teque
        self.length += 1

        #updating middle pointer
        self.update_middle("back")

    def push_front(self, x):
        v = Node(x, prev=None, next=self.head)
        self.is_empty(v)
        self.head.prev = v
        self.head = v

        #updating length of teque
        self.length += 1

        #updating middle pointer
        self.update_middle("front")

    #Update middle-pointer
    def update_middle(self, direction):

        #middle only moves if length is odd
        #when pushing front
        if (self.length % 2) == 1 and direction == "front":
            self.middle = self.middle.prev

        #middle only moves if length is even
        #when pushing back
        elif (self.length % 2) == 0 and direction == "back":
            self.middle = self.middle.next

    def push_middle(self, x):
        #check for empty list
        if self.length == 0:
            v = Node(x)
            self.is_empty(v)

            self.length += 1
            return

        #check for list with one element
        elif self.length == 1:
            v = Node(x, prev=self.middle, next=None)
            self.middle.next = v
            self.middle = v
            self.tail = v
            self.length += 1
            return

        #check for even length list
        elif (self.length % 2) == 0:
            v = Node(x, prev=self.middle.prev, next=self.middle)

            #connect adjacent
            #nodes to v
            self.middle.prev.next = v
            self.middle.prev = v
            self.length += 1
            self.middle = v

        #check for odd length list
        else:
            v = Node(x, prev = self.middle, next = self.middle.next)

            #connect adjacent
            #nodes to v
            self.middle.next.prev = v
            self.middle.next = v
            self.length += 1
            self.middle = v

    def get(self, index):
        #Checking the index
        if (self.length > 0) and (0 <= index < self.length):
            temp = self.head
            for i in range(index):
                temp = temp.next
            return temp.value
        else:
            raise IndexError("Index is out of range!")


class Node():
    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.next = next
        self.prev = prev


list = ["push_back", "push_front", "push_middle", "get"]


if __name__ == "__main__":
    answer = Teque()
    for line in  sys.stdin:
        func = line.split(" ")
        if (len(func) == 2):
            func[1] = int(func[1])
            if func[0] == list[0]:
                answer.push_back(func[1])
            elif func[0] == list[1]:
                answer.push_front(func[1])
            elif func[0] == list[2]:
                answer.push_middle(func[1])
            elif func[0] == list[3]:
                print(f"{answer.get(func[1])}", sep='\n')
            else:
                raise NameError("Function is not valid!")
