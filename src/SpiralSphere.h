#ifndef SPIRALSPHERE_H
#define SPIRALSPHERE_H

#include "utils.h"
#include <tuple>

class SpiralSphere {
private:
    double theta_period, phi_period;
    double r;
    double tilt_x, tilt_y, tilt_z;
    double d_tilt_x, d_tilt_y, d_tilt_z;

public:
    SpiralSphere(double theta_period = 2 * PI, double phi_period = PI, double r = 1,
                 double tilt_x = PI / 6, double tilt_y = PI / 6, double tilt_z = PI / 6,
                 double d_tilt_x = 0.0001, double d_tilt_y = 0, double d_tilt_z = 0);

    std::tuple<double, double, double> getPoint(double t);
    void rotate();
};

#endif // SPIRALSPHERE_H