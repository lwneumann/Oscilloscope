#include "shapeContainer.h"
#include <stdexcept>

// Constructor
ShapeContainer::ShapeContainer() : waveGenerator(nullptr), projectionType(ORTH) {}

// Destructor
ShapeContainer::~ShapeContainer() {
    // Delete all shapes and weights in the container
    for (int i = 0; i < shapes.getSize(); i++) {
        delete shapes[i];
        delete weights[i];
    }
    // Delete the wave generator if it exists
    delete waveGenerator;
}

// Add a shape to the container with an optional weight
void ShapeContainer::addShape(Shape* shape, float* weight) {
    if (!shape) {
        throw std::invalid_argument("Shape cannot be null");
    }
    if (weight && (*weight < 0.0f || *weight > 1.0f)) {
        throw std::invalid_argument("Weight must be in the range [0, 1]");
    }
    shapes.push_back(shape);
    // Store a copy of the weight or nullptr
    weights.push_back(weight ? new float(*weight) : nullptr);
}

// Remove a shape from the container by index
void ShapeContainer::removeShape(int index) {
    if (index < 0 || index >= shapes.getSize()) {
        throw std::out_of_range("Index out of range");
    }
    // Free the memory for the shape and weight
    delete shapes[index];
    delete weights[index];

    shapes.deleteAt(index);
    weights.deleteAt(index);
}

// Set the projection type
void ShapeContainer::setProjectionType(ProjectionType type) {
    projectionType = type;
}

// Projection method
std::tuple<double, double, double> ShapeContainer::projection(std::tuple<double, double, double> point) {
    double x = std::get<0>(point);
    double y = std::get<1>(point);
    double z = std::get<2>(point);

    switch (projectionType) {
        case ORTH:
            // Orthographic projection (ignore z)
            return {x, y, 0.0};
        case PERC:
            // Perspective projection (scale x and y by z)
            if (z != 0.0) {
                return {x / z, y / z, z};
            } else {
                return {x, y, z}; // Avoid division by zero
            }
        default:
            throw std::runtime_error("Unknown projection type");
    }
}

// Distribute `t` across shapes based on weights and get their points
std::tuple<double, double, double> ShapeContainer::getPoint(double t) {
    if (shapes.isEmpty()) {
        throw std::runtime_error("No shapes in the container");
    }

    double totalWeight = 0.0;
    int nullWeightCount = 0;

    // Calculate total weight and count shapes with null weights
    for (int i = 0; i < weights.getSize(); i++) {
        if (weights[i]) {
            totalWeight += *weights[i];
        } else {
            nullWeightCount++;
        }
    }

    // Ensure total weight does not exceed 1.0
    if (totalWeight > 1.0) {
        throw std::runtime_error("Total weight of shapes exceeds 1.0");
    }

    // Calculate the remaining `t` to be evenly distributed among null-weight shapes
    double remainingT = t * (1.0 - totalWeight);
    double nullWeightShare = (nullWeightCount > 0) ? remainingT / nullWeightCount : 0.0;

    double x = 0.0, y = 0.0, z = 0.0;
    double allocatedT = 0.0;

    for (int i = 0; i < shapes.getSize(); i++) {
        double shapeT = 0.0;

        if (weights[i]) {
            // Allocate `t` based on the weight
            shapeT = t * (*weights[i]);
        } else {
            // Allocate evenly among null-weight shapes
            shapeT = nullWeightShare;
        }

        // Normalize `shapeT` to [0, 1] for the current shape
        double normalizedT = (shapeT > 0.0) ? allocatedT / shapeT : 0.0;
        auto point = shapes[i]->getPoint(normalizedT);

        x += std::get<0>(point);
        y += std::get<1>(point);
        z += std::get<2>(point);

        allocatedT += shapeT;
    }

    return {x, y, z};
}