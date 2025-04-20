#ifndef DYNAMICARRAY_H
#define DYNAMICARRAY_H

#include <stdexcept>

template <typename T>
class DynamicArray {
private:
    T* array;              // Pointer to the array
    int size;              // Current number of elements
    int capacity;          // Maximum capacity of the array

    void growArray();      // Double the capacity
    void shrinkArray();    // Halve the capacity

public:
    DynamicArray();                          // Default constructor
    DynamicArray(int capacity);              // Constructor with initial capacity
    ~DynamicArray();                         // Destructor

    int getSize() const;                     // Get the current size
    int getCapacity() const;                 // Get the current capacity
    bool isEmpty() const;                    // Check if the array is empty

    void push_back(const T& value);          // Add an element to the end
    void pop_back();                         // Remove the last element
    void insertAt(int index, const T& value);// Insert an element at a specific index
    void deleteAt(int index);                // Delete an element at a specific index

    T& operator[](int index);                // Access element by index
    const T& operator[](int index) const;    // Access element by index (const version)
};

#include "dynamicArray.tpp"

#endif // DYNAMICARRAY_H