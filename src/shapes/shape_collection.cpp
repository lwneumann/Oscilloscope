#include "shape_collection.h"

// Add a shape to the collection
void ShapeCollection::addShape(const Shape& shape) {
    shapes.push_back(shape);
}

// Pop a point from the buffer
std::vector<double> ShapeCollection::popPoint() {
    if (buffer.empty()) {
        // Refill the buffer if it's empty
        refillBuffer();
    }

    // Retrieve and remove the front point from the buffer
    std::vector<double> point = buffer.front();
    buffer.pop();
    return point;
}

// Refill the buffer by calling getFrame from all shapes
void ShapeCollection::refillBuffer() {
    for (const auto& shape : shapes) {
        // Generate points using the shape's getFrame function
        std::vector<std::vector<double>> shapePoints = shape.getFrame(shape.num_points);

        // Get transformed points
        // TODO - apply shaders and such
        for (auto& point : shapePoints) {
            // Scale and translate x and y
            point[0] = point[0] * shape.scale + shape.x;
            point[1] = point[1] * shape.scale + shape.y;
            // Z is there too but for now we just use orthographic projection
            buffer.push(point);
        }
    }
}