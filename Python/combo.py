import math

class Node:
    def __init__(self,x,prev=None,next=None):
        self.x = x
        self.prev = prev
        self.next = next
        self.value = x

class NewNode:
    def __init__(self,x,prev,next):
        self.x = x
        self.prev = prev
        self.next = next
        self.value = x

class Teque:
    def __init__(self):
        self.head = None
        self.tail = None
        self.middle = None
        self.length = 0

    def empty(self,v):
        if self.head is None:
            self.head = v
            self.tail = v

    def push_back(self,x):
        v = Node(x)
        self.empty(v)
        v = NewNode(x, prev=self.tail, next=None)
        self.tail = v

        self.length += 1

    def push_front(self,x):
        v = Node(x)
        self.empty(v)
        v = NewNode(x, prev=None, next=self.head)
        self.head = v

        self.length += 1


list = Teque()
list.push_front(1)
list.push_back(4)
list.push_front(5)
list.push_back(8)
list.push_middle(7)
