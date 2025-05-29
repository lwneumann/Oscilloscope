#include "utils.h"
#include <cmath>
#include "tuple"
#include <iostream>


namespace utils {
    int sgn(double value) {
        return (value > 0) - (value < 0);
    }

    double to_square_wave(double t, double period) {
        return sgn(std::sin((2 * PI * t) / period));
    }

    std::tuple<double, double, double> rotatePoint(double x, double y, double z, double tilt_x, double tilt_y, double tilt_z) {
        // Apply X-axis rotation
        double y_x = y * cos(tilt_x) - z * sin(tilt_x);
        double z_x = y * sin(tilt_x) + z * cos(tilt_x);
        // Apply Y-axis rotation
        double x_y = x * cos(tilt_y) + z_x * sin(tilt_y);
        double z_y = -x * sin(tilt_y) + z_x * cos(tilt_y);
        // Apply Z-axis rotation
        double x_z = x_y * cos(tilt_z) - y_x * sin(tilt_z);
        double y_z = x_y * sin(tilt_z) + y_x * cos(tilt_z);
        
        return std::make_tuple(x_z, y_z, z_y);
    }
}
