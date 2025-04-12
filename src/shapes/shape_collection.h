#ifndef SHAPE_COLLECTION_H
#define SHAPE_COLLECTION_H

#include <vector>
#include <queue>
#include <functional>

// Shape struct
struct Shape {
    // "getFrame" is the function in each shape to generate a point
    std::function<std::vector<std::vector<double>>(int)> getFrame;
    // Scale of the shape
    double scale;
    // X offset
    double x;
    // Y offset
    double y;
    // Number of points per shape per frame
    int num_points;
};

// ShapeCollection class
class ShapeCollection {
private:
    // Collection of shapes
    std::vector<Shape> shapes;
    // Queue to hold points (x, y, z)
    std::queue<std::vector<double>> buffer;

public:
    // Constructor
    ShapeCollection() = default;

    // Add a shape to the collection
    void addShape(const Shape& shape);

    // Pop a point from the buffer
    std::vector<double> popPoint();

    // Refill the buffer by calling getFrame from all shapes
    void refillBuffer();
};

#endif // SHAPE_COLLECTION_H