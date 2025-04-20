#ifndef COMPONENT_H
#define COMPONENT_H

#include "dynamicArray.h" // Include the DynamicArray class

enum ComponentMode { CONSTANT, WAVEFORM };
enum OperationMode { SUM, PRODUCT };

class Component {
public:
    // Attributes
    ComponentMode compMode = CONSTANT;
    OperationMode opMode = SUM;
    double const_value = 0.0;
    Component offset = Component(0.0);
    Component rotate_threshold = Component(0.9);
    DynamicArray<Component> children;

    // Constructors
    // -- Default
    Component() : children(1) {
        children[0] = Component(0.0);
    }
    // -- Constants
    Component(double value)
        : is_constant(true), const_value(value), children(1) {
        children[0] = Component(0.0);
    }

    // Destructor (default behavior is fine)? is not?
    ~Component() = default;

    // Copy Constructor
    Component(const Component& other)
        : is_constant(other.is_constant),
          const_value(other.const_value),
          offset(other.offset),
          rotate_threshold(other.rotate_threshold),
          children(other.children) {}

    // Assignment Operator
    Component& operator=(const Component& other) {
        if (this == &other) return *this; // Handle self-assignment

        is_constant = other.is_constant;
        const_value = other.const_value;
        offset = other.offset;
        rotate_threshold = other.rotate_threshold;
        children = other.children;

        return *this;
    }

    // Print details for debugging
    void printDetails() const {
        if (is_constant) {
            std::cout << "Constant Component with value: " << const_value << std::endl;
        } else {
            std::cout << "Non-constant Component" << std::endl;
            std::cout << "  Offset: " << offset.const_value << std::endl;
            std::cout << "  Rotate Threshold: " << rotate_threshold.const_value << std::endl;
        }
        std::cout << "Number of children: " << children.getSize() << std::endl;
        for (int i = 0; i < children.getSize(); ++i) {
            std::cout << "  Child " << i << " const_value: " << children[i].const_value << std::endl;
        }
    }
};

#endif // COMPONENT_H