#include <iostream>
#include <cassert>
#include <stdexcept>
#include <vector>

struct Node {
  int value;
  Node *next;

  Node(int n) {
    value = n;
    next = nullptr;
  }

  Node(int n, Node *p) {
    value = n;
    next = p;
  }
};

class CircLinkedList {
  /*Class for circular linked list. Each node has a pointer to the next,
    and the last node points to head.
  */
  private:
    Node *head;

  public:
    int size;

    CircLinkedList() {
      head = nullptr;
      size = 0;
    }

    CircLinkedList(int n) {
      head = nullptr;
      size = 0;
      for (int i=1; i<n+1; i++) {
        append(i);
      }
    }

    ~CircLinkedList() {
      Node *current = head;
      Node *next = current->next;
      while (size > 0) {
        next = current->next;
        delete current;
        current = next;
        size--;
      }
    }

    int& operator[](int n) {
      if (size == 0) {
        throw std::out_of_range("The list is empty!");
      }
      return get_node(n)->value;
    }

    Node* get_node(int index) {
      Node *current = head;
      for (int i = 0; i < index; i++) {
        current = current->next;
      }
      return current;
    }

    void append(int value) {
      if (size==0) {
        Node *tmp = new Node(value);
        tmp->next = tmp;
        head = tmp;
        size++;
      } else {
        Node *current = head;
        for (int i = 0; i < size-1; i++) {
            current = current->next;
        }
        current->next = new Node(value, head);
        size++;
      }
    }

    void print() {
      if (size == 0) {
        std::cout << "[]" << '\n';
        return;
      }
      std::cout << "[";
      for (int i=0; i<size-1; i++) {
        std::cout << get_node(i)->value << ",";
      }
      std::cout << get_node(size-1)->value << "]" << std::endl;
    }

    void remove_node(Node *p) {
      Node *current = p;
      //move current to the node previous to p
      for (int i=0; i<size-1; i++) {
        current = current->next;
      }
      Node *prev = current;
      Node *next = p->next;
      prev->next = next;
      size--;
    }

    std::vector<int> josephus_sequence(int k) {
      std::vector<int> josephus_vec;
      //get the k-th element and remove it
      Node *tmp = get_node(k-1);
      josephus_vec.push_back(tmp->value);
      Node *current = tmp->next;
      remove_node(tmp);
      //current is now at the k+1-th element

      while (size > 0) {
        //move to the next element to be removed
        for (int i=1; i<k; i++) {
          current = current->next;
        }
        // extract value, move to the node after the one being removed,
        // remove current node
        josephus_vec.push_back(current->value);
        Node *tmp = current;
        current = tmp->next;
        remove_node(tmp);
      }
      return josephus_vec;
    }
};


int last_man_standing(int n, int k) {
  /*Solves the Josephus problem with a given int n and int k, where n
  equals the number of participants and k equals the step length. Returns
  the safe position/the last man standing.
  */
  CircLinkedList josephus(n);
  std::vector<int> seq = josephus.josephus_sequence(k);
  return seq[seq.size()-1];
}

void test_josephus_sequence() {
  CircLinkedList josephus(6);
  josephus.print();
  std::vector<int> vec = josephus.josephus_sequence(3);
  josephus.print();
  assert(vec[vec.size()-1] == 1);
}

void test_append_and_indexing() {
  CircLinkedList test;
  for (int i=0; i<5; i++) {
    test.append(i);
  }
  assert(test.size == 5);
  assert(test[0] == 0);
  assert(test[4] == 4);
}

void test_print() {
  CircLinkedList test;
  test.print();
  for (int i=1; i<6; i++) {
    test.append(i);
  }
  test.print();
}


int main() {
  test_append_and_indexing();
  test_print();
  test_josephus_sequence();
  int res = last_man_standing(68, 7);
  std::cout << res << '\n';
  return 0;
}
