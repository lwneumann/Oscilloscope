#include <iostream>
#include <stdexcept>

// Default constructor
template <typename T>
DynamicArray<T>::DynamicArray() : size(0), capacity(1) {
    array = new T[capacity];
}

// Constructor with initial capacity
template <typename T>
DynamicArray<T>::DynamicArray(int capacity) : size(0), capacity(capacity) {
    array = new T[capacity];
}

// Destructor
template <typename T>
DynamicArray<T>::~DynamicArray() {
    delete[] array;
}

// Get the current size
template <typename T>
int DynamicArray<T>::getSize() const {
    return size;
}

// Get the current capacity
template <typename T>
int DynamicArray<T>::getCapacity() const {
    return capacity;
}

// Check if the array is empty
template <typename T>
bool DynamicArray<T>::isEmpty() const {
    return size == 0;
}

// Add an element to the end
template <typename T>
void DynamicArray<T>::push_back(const T& value) {
    if (size == capacity) {
        growArray();
    }
    array[size++] = value;
}

// Remove the last element
template <typename T>
void DynamicArray<T>::pop_back() {
    if (size == 0) {
        throw std::out_of_range("Array is empty");
    }
    size--;
    if (size <= capacity / 2) {
        shrinkArray();
    }
}

// Insert an element at a specific index
template <typename T>
void DynamicArray<T>::insertAt(int index, const T& value) {
    if (index < 0 || index > size) {
        throw std::out_of_range("Index out of range");
    }
    if (size == capacity) {
        growArray();
    }
    for (int i = size; i > index; i--) {
        array[i] = array[i - 1];
    }
    array[index] = value;
    size++;
}

// Delete an element at a specific index
template <typename T>
void DynamicArray<T>::deleteAt(int index) {
    if (index < 0 || index >= size) {
        throw std::out_of_range("Index out of range");
    }
    for (int i = index; i < size - 1; i++) {
        array[i] = array[i + 1];
    }
    size--;
    if (size <= capacity / 2) {
        shrinkArray();
    }
}

// Access element by index
template <typename T>
T& DynamicArray<T>::operator[](int index) {
    if (index <= -size || index >= size) {
        throw std::out_of_range("Index out of range");
    }
    if (index < 0) {
        index += size; // Reverse indexing
    }
    return array[index];
}

// Access element by index (const version)
template <typename T>
const T& DynamicArray<T>::operator[](int index) const {
    if (index <= -size || index >= size) {
        throw std::out_of_range("Index out of range");
    }
    if (index < 0) {
        index += size; // Reverse indexing
    }
    return array[index];
}

// Double the capacity
template <typename T>
void DynamicArray<T>::growArray() {
    capacity *= 2;
    T* temp = new T[capacity];
    for (int i = 0; i < size; i++) {
        temp[i] = array[i];
    }
    delete[] array;
    array = temp;
}

// Halve the capacity
template <typename T>
void DynamicArray<T>::shrinkArray() {
    capacity = std::max(1, capacity / 2);
    T* temp = new T[capacity];
    for (int i = 0; i < size; i++) {
        temp[i] = array[i];
    }
    delete[] array;
    array = temp;
}