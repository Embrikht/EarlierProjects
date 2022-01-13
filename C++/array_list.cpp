#include <cassert>
#include <stdexcept>
#include <iostream>
#include <math.h>
#include <vector>

class ArrayList {
  /*
  Dynamic array with maximum capacity.
  The array is store in data, which points to the start of the array, size
  keeps track of the number of elements.
  The maximum capacity is stored in capacity and may be increased og decreased
  according to the length of the list.
  */
private:
  int *data;
  int capacity;

  void resize() {
    // Double capacity
    capacity *= 2;
    int *newdata = new int[capacity];
    for (int i = 0; i < size; i++) {
      newdata[i] = data[i];
    }
    delete[] data;
    data = newdata;
  }

public:
  int size;

  ArrayList() {
    size = 0;
    capacity = 1;
    data = new int[capacity];
  }

  ArrayList(std::vector<int> v) {
    size = v.size();
    capacity = v.size();
    data = new int[capacity];
    for (int i=0; i<size; i++) {
      data[i] = v[i];
    }
  }

  ~ArrayList() {
    delete[] data;
  }

  int get_capacity() {
    // This method is only meant to be used to
    // test shrink_to_fit
    return capacity;
  }

  int length() {
    return size;
  }

  int pop(int n) {
    // Remove and return the n-th element of the list.
    int a = data[n];
    remove(n);
    return a;
  }

  int pop() {
    // Remove and return the last element of the list.
   return pop(size-1);
  }

  int& operator[](int n) {
    if (n >= 0 && n < size) {
      return data[n];
    }
    else {
      throw std::out_of_range("Index out of range!");
    }
  }

  void append(int n) {
    if (size >= capacity) {
      resize();
    }
    data[size] = n;
    size += 1;
  }

  void print() {
    if (size == 0) {
      std::cout << "[]" << '\n';
      return;
    }
    std::cout << "[";
    for (int i=0; i<size-1; i++) {
      std::cout << data[i] << ", ";
    }
    std::cout << data[size-1] << "]" << '\n';
  }

  void insert(int val, int index) {
    // Insert val at index
    if (0 <= index && index <= size) {
      append(0);
      for (int i = size; i>index; i--) {
        data[i] = data[i-1];
      }
      data[index] = val;
    }
    else {
      throw std::out_of_range("Index out of range!");
    }
  }

  void remove(int n) {
    if (0 <= n && n < size) {
      for (int i = n; i < size; i++) {
        data[i] = data[i+1];
      }
      size -= 1;
      if (size <= 0.25*capacity) {
        shrink_to_fit();
      }
    } else {
      throw std::out_of_range("Index out of range!");
    }
  }

  void shrink_to_fit() {
    // Shrink the capacity so as not
    // to occupy unnecessarily much memory.
    while (2*size <= capacity) {
      capacity /= 2;
    }
  }
};


bool is_prime(int n) {
  // Checks if n is prime. Returns true if n is prime,
  // false if n is not prime (composite).
  if (n == 1) {
    return false;
  }
  if (n == 2 || n == 3) {
    return true;
  }
  if (n%2 == 0) {
    return false;
  }
  for (int i=3; i<=floor(sqrt(n)); i += 2) {
    if (n%i == 0) {
      return false;
    }
  }
  return true;
}

void test_resize() {
  //A newly created list should return the same
  ArrayList test;
  assert(test.length() == 0);
  test.append(1);
  assert(test.size == 1);
  test.append(2);
  assert(test.size == 2);
}

void test_print() {
  ArrayList test;
  test.print();
  test.append(33);
  test.append(4);
  test.append(0);
  test.print();
}

void test_ArrayList() {
  ArrayList primes;
  int i = 2;
  while (primes.size < 10) {
    if (is_prime(i)) {
      primes.append(i);
    }
    i++;
  }
  primes.print();
}

void test_vector_init() {
  ArrayList primes({2, 3, 5, 8, 11});
  primes.print();
}

void test_operator() {
  ArrayList list({1, 2, 3, 4, 5});
  assert(list[1] == 2);
  list.print();
  list[2] = 4;
  assert(list[2] == 4);
  list.print();
}

void test_insert() {
  ArrayList list({1, 2, 3, 4, 5});
  list.print();
  list.insert(10, 2);
  list.print();
  list.insert(12, 6);
  list.print();
}

void test_remove() {
  ArrayList list({1, 2, 3, 4, 5, 8, 10, 20});
  list.print();
  list.remove(6);
  list.print();
}

void test_pop() {
  ArrayList list({1, 2, 3, 4, 5, 8, 10, 20});
  assert(list.pop(4) == 5);
  list.print();
  assert(list.pop() == 20);
  list.print();
}

void test_shrinking_array() {
  ArrayList list({11, 24, 26, 19});
  list.append(2);
  list.remove(2);
  list.remove(3);
  assert(list.get_capacity() == 8);
  list.shrink_to_fit();
  assert(list.get_capacity() == 4);
}

void test_automatic_shrink() {
  ArrayList list({1, 2, 3, 4, 5, 6, 7, 8});
  assert(list.get_capacity() == 8);
  for (int i = 7; i >= 2; i--) {
    list.remove(i);
  }
  assert(list.get_capacity() == 2);
}


int main() {
  //Using this for testing
  /*
  test_resize();
  test_print();
  test_ArrayList();
  test_vector_init();
  test_operator();
  test_insert();
  test_remove();
  test_pop();
  test_shrinking_array();
  test_automatic_shrink();
  */
  return 0;
}
