#ifndef MUSHROOM_H
#define MUSHROOM_H

#include "utils.h"
#include <tuple>

class mushroom {
private:
    double theta_period, phi_period;
    double r, cap_r;
    double wiggle, d_wiggle;
    double tilt_x, tilt_y, tilt_z;
    double d_tilt_x, d_tilt_y, d_tilt_z;

public:
    mushroom(double theta_period = 128.0 * PI, double phi_period = PI,
                double r = 0.1, double cap_r = 0.5,
                double wiggle = 0.0, double d_wiggle = 0.00001,
                double tilt_x = 0.5, double tilt_y = 0.0, double tilt_z = 0.0,
                double d_tilt_x = 0.0, double d_tilt_y = 0.0, double d_tilt_z = 0.0);

    std::tuple<double, double, double> getPoint(double t);
    void rotate();
};

#endif // MUSHROOM_H