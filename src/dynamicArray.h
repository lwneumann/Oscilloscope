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

    // Handle capacity
    void growArray();
    void shrinkArray();

public:
// Default constructor
    DynamicArray();
    // Constructor with initial capacity
    DynamicArray(int capacity);
    // Destructor
    ~DynamicArray();

    int getSize() const;
    int getCapacity() const;
    bool isEmpty() const;

    // Add an element to end
    void push_back(const T& value);
    // Remove last element
    void pop_back();
    // Insert at a specific index
    void insertAt(int index, const T& value);
    // Delete at a specific index
    void deleteAt(int index);

    // Index
    T& operator[](int index);
    // Index (const version)
    const T& operator[](int index) const;
};

#include "dynamicArray.tpp"

#endif // DYNAMICARRAY_H