#ifndef SHAPECONTAINER_H
#define SHAPECONTAINER_H

#include "dynamicArray.h"
#include "WaveGenerator.h"
#include <tuple>
#include <vector>

class Shape {
public:
    virtual std::tuple<double, double, double> getPoint(double t) = 0;
    virtual ~Shape() = default;
};

class ShapeContainer {
public:
    ShapeContainer();
    ~ShapeContainer();

    // Add a shape with an optional weight
    void addShape(Shape* shape, float* weight = nullptr);
    // Remove a shape by index
    void removeShape(int index);

    // Set the projection type. Maybe change names later.
    enum ProjectionType { ORTH, PERC };
    void setProjectionType(ProjectionType type);

    // Projection such as orthographic, or perspective
    std::tuple<double, double, double> projection(std::tuple<double, double, double> point);

    // Distribute t across shapes based on weights and get their points
    std::tuple<double, double, double> getPoint(double t);

private:
    // Dynamic array of shapes
    DynamicArray<Shape*> shapes;
    // Dynamic array of weights (nullptr or float in [0, 1])
    DynamicArray<float*> weights;
    // Optional internal WaveGenerator
    WaveGenerator* waveGenerator;
    // Projection
    ProjectionType projectionType = ORTH;
};

#endif // SHAPECONTAINER_H