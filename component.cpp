#include "component.h"

// === Constructors
// -- Default (CONTAINER)
Component::Component() 
    : mode(CONTAINER), const_value(0.0), children(1) {
    children[0] = Component(0.0);
}
// -- Constant
Component::Component(double value)
    : mode(CONSTANT), const_value(value), children(1) {
    children[0] = Component(0.0);
}
// -- Waveform
Component::Component(WaveGenerator::WaveType waveType, double frequency, double amplitude, double phase)
    : mode(WAVEFORM), waveGen(waveType, frequency, amplitude, phase), children(1) {
    children[0] = Component(0.0);
}

// Copy constructor
Component::Component(const Component& other)
    : mode(other.mode),
      const_value(other.const_value),
      opMode(other.opMode),
      offset(other.offset),
      rotate_threshold(other.rotate_threshold),
      children(other.children),
      waveGen(other.waveGen) {}

// Assignment operator
Component& Component::operator=(const Component& other) {
    if (this == &other) return *this;

    mode = other.mode;
    const_value = other.const_value;
    opMode = other.opMode;
    offset = other.offset;
    rotate_threshold = other.rotate_threshold;
    children = other.children;
    waveGen = other.waveGen;

    return *this;
}

// Evaluate the component's value at time t
double Component::evaluate(double t) {
    if (mode == CONSTANT) {
        return const_value;
    } else if (mode == WAVEFORM) {
        return waveGen.generate(t);
    } else if (mode == CONTAINER) {
        // Combine child values based on opMode
        double result = (opMode == PRODUCT) ? 1.0 : 0.0;
        for (int i = 0; i < children.getSize(); ++i) {
            double childValue = children[i].evaluate(t);
            if (opMode == SUM) {
                result += childValue;
            } else if (opMode == PRODUCT) {
                result *= childValue;
            }
        }
        return result;
    }

    // Default fallback if no mode or children
    return 0.0;
}

// Print details for debugging
void Component::printDetails() const {
    if (mode == CONSTANT) {
        std::cout << "Constant Component with value: " << const_value << std::endl;
    } else if (mode == WAVEFORM) {
        std::cout << "Waveform Component with type: " << waveGen.getWaveTypeAsString() << std::endl;
        std::cout << "  Frequency: " << waveGen.getFrequency() << std::endl;
        std::cout << "  Amplitude: " << waveGen.getAmplitude() << std::endl;
        std::cout << "  Phase: " << waveGen.getPhase() << std::endl;
    } else if (mode == CONTAINER) {
        std::cout << "Container Component:" << std::endl;
        std::cout << "  Operation Mode: " << (opMode == SUM ? "SUM" : "PRODUCT") << std::endl;
        std::cout << "  Number of Children: " << children.getSize() << std::endl;
        for (int i = 0; i < children.getSize(); ++i) {
            std::cout << "    Child " << i << ": ";
            children[i].printDetails();
        }
    }
}