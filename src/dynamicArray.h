#ifndef DYNAMICARRAY_H
#define DYNAMICARRAY_H

#include <stdexcept>

template <typename T>
class DynamicArray {
private:
    // Pointer to the array
    T* array;
    // Current number of elements
    int size;
    // Maximum capacity of the array
    int capacity;

    // Double the capacity
    void growArray();
    // Halve the capacity
    void shrinkArray();

public:
// Default constructor
    DynamicArray();
    // Constructor with initial capacity
    DynamicArray(int capacity);
    // Destructor
    ~DynamicArray();

    // Get the current size
    int getSize() const;
    // Get the current capacity
    int getCapacity() const;
    // Check if the array is empty
    bool isEmpty() const;

    // Add an element to the end
    void push_back(const T& value);
    // Remove the last element
    void pop_back();
    // Insert an element at a specific index
    void insertAt(int index, const T& value);
    // Delete an element at a specific index
    void deleteAt(int index);

    // Access element by index
    T& operator[](int index);
    // Access element by index (const version)
    const T& operator[](int index) const;
};

#include "dynamicArray.tpp"

#endif // DYNAMICARRAY_H