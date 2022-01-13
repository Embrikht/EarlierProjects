#include <iostream>
#include <cassert>
#include <stdexcept>
#include <vector>


struct Node {
  int value;
  Node *next;
  Node *prev;

  Node(int n, Node *p, Node *q) {
      value = n;
      next = p;
      prev = q;
  }

  Node(int n) {
    value = n;
    next = nullptr;
    prev = nullptr;
  }
};

class LinkedList {
  /*
  Doubly linked list with tail reference. Each node has a pointer to the
  next and previous node.
  */
  private:
    Node *head;
    Node *tail;

  public:
    LinkedList() {
      head = nullptr;
      tail= nullptr;
    }

    LinkedList(std::vector<int> vec) {
      head = nullptr;
      tail = nullptr;
      for (int p: vec) {
        append(p);
      }
    }


    int length() {
      // Returns the number of elements in the list.
      Node *current = head;
      int count = 0;

      while (current != nullptr) {
        count++;
        current = current->next;
      }
      return count;
    }

    int& operator[](int n) {
      return get_node(n)->value;
    }

    void append(int n) {
      if (head == nullptr) {
        head = new Node(n);
        tail = head;
        return;
      }
      Node *current = tail;
      tail = new Node(n, nullptr, current);
      current->next = tail;
    }

    void print() {
      Node *current = head;
      if (current == nullptr) {
        std::cout << "[]" << std::endl;
        return;
      }
      std::cout << "[";
      while (current->next != nullptr) {
        std::cout << current->value << ", ";
        current = current->next;
      }
      std::cout << current->value << "]" << std::endl;
    }

    Node* get_node(int index) {
      if ((0 <= index) && (index < length())){
        if (2*index <= length()) {
          Node *current = head;
          for (int i=0; i<index; i++) {
            current = current->next;
          }
          return current;
        }
        else {
          Node *current = tail;
          for (int i=length(); i>index+1; i--) {
            current = current->prev;
          }
          return current;
        }
      }
      else {
        throw std::out_of_range("Index is out of range!");
      }
    }

    void insert(int value, int index) {
      // Insert value at index.
      Node *prev;
      if ((length() == 0) || index == length()) {
        append(value);
        return;
      }
      Node *next = get_node(index);
      if (index == 0) {
        head = new Node(value, next, nullptr);
      }
      else {
        prev = get_node(index-1);
        prev->next = new Node(value, next, prev);
      }
    }

    void remove(int index) {
      if (index == 0) {
        Node *tmp = head;
        delete head;
        head = tmp->next;
        head->prev = nullptr;
        return;
      }
      if (index == length()-1) {
        Node *tmp = tail;
        delete tail;
        tail = tmp->prev;
        tail->next = nullptr;
        return;
      }

      Node *prev = get_node(index-1);
      Node *next = get_node(index+1);
      delete get_node(index);
      prev->next = next;
      next->prev = prev;
    }

    int pop(int index) {
       // Remove and return the removed value.
       int res = get_node(index)->value;
       remove(index);
       return res;
    }

    int pop() {
      // Remove and return the last element. 
      int res = pop(length()-1);
      return res;
    }

  ~LinkedList() {
    Node *current = head;
    Node *next = current->next;
    while (current != nullptr) {
      next = current->next;
      delete current;
      current = next;
    }
  }
};


void test_append() {
  LinkedList test;
  test.print();
  test.append(10);
  test.print();
  test.append(20);
  test.print();
}

void test_length() {
  LinkedList test;
  assert(test.length() == 0);
  test.append(1);
  assert(test.length() == 1);
  test.append(2);
  assert(test.length() == 2);
}

void test_indexing() {
  LinkedList test;
  for (int i=1; i<11; i++) {
    test.append(i);
  }
  assert(test[3] == 4);
  assert(test[0] == 1);
  assert(test[9] == 10);
  assert(test[6] == 7);
}

void test_insert() {
  LinkedList test;
  for (int i=1; i<11; i++) {
    test.append(i);
  }
  test.insert(10, 4);
  assert(test[4] == 10);
  test.insert(100, 11);
  assert(test[11] == 100);
  test.insert(80, 0);
  assert(test[0] == 80);
}

void test_remove() {
  LinkedList test;
  for (int i=1; i<11; i++) {
    test.append(i);
  }
  test.remove(5);
  test.remove(0);
  test.remove(7);
  test.print();
}

void test_pop() {
  LinkedList test;
  for (int i=1; i<11; i++) {
    test.append(i);
  }
  assert(test.pop(5) == 6);
  assert(test.pop() == 10);
}

void test_vectorinit() {
  LinkedList vec({1, 2, 3, 4, 5});
  vec.print();
}


int main() {
  test_append();
  test_length();
  test_indexing();
  test_insert();
  test_remove();
  test_pop();
  test_vectorinit();
  return 0;
}
