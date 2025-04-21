#ifndef UTILS_H
#define UTILS_H

#include <tuple>

// Define constants
#ifndef PI
#define PI 3.14159265358979323846
#endif

#ifndef ROTATE_THRESHOLD
#define ROTATE_THRESHOLD 0.9
#endif

// Later add lerp, distance and some other functions to a utils.cpp
namespace utils {
    int sgn(double value);
    double to_square_wave(double t, double period = 1);
    std::tuple<double, double, double> rotatePoint(double x, double y, double z, double tilt_x, double tilt_y, double tilt_z);
}

#endif // UTILS_H