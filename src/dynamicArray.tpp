#include <iostream>
#include <stdexcept>

template <class T>
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
    if (index < 0 || index >= size) {
        throw std::out_of_range("Index out of range");
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
        // Reverse indexing
        index += size;
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