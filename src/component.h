#ifndef COMPONENT_H
#define COMPONENT_H

#include "dynamicArray.h"
#include "waveGenerator.h"


class Component {
public:
    enum ComponentMode { CONSTANT, WAVEFORM, CONTAINER };
    enum OperationMode { SUM, PRODUCT };
    // Attributes
    ComponentMode mode = CONSTANT;
    double const_value = 0.0;
    OperationMode opMode = SUM;
    Component offset = Component(0.0);
    Component rotate_threshold = Component(0.9);
    DynamicArray<Component> children;
    WaveGenerator waveGen;

    // Constructors
    // -- Default (CONTAINER)
    Component();
    // -- Constant
    Component(double value);
    // -- Waveform
    Component(WaveGenerator::WaveType waveType, double frequency, double amplitude, double phase);

    // Destructor
    ~Component() = default;

    // Copy constructor
    Component(const Component& other);

    // Assignment operator
    Component& operator=(const Component& other);

    // Evaluate the component's value at time t
    double evaluate(double t);

    // Print details for debugging
    void printDetails() const;
};

#endif // COMPONENT_H