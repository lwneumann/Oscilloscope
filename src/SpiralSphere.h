#ifndef SPIRALSPHERE_H
#define SPIRALSPHERE_H

#include <tuple>

class SpiralSphere {
private:
    double theta_period, phi_period;
    double r;
    double tilt_x, tilt_y, tilt_z;
    double d_tilt_x, d_tilt_y, d_tilt_z;

public:
    // Constructor
    SpiralSphere(double theta = 0, double phi = 0, double d_theta = 0.02, double d_phi = 0.001, double r = 1,
                 double tilt_x = M_PI / 6, double tilt_y = M_PI / 6, double tilt_z = M_PI / 6,
                 double d_tilt_x = 0.0001, double d_tilt_y = 0, double d_tilt_z = 0);

    // Returns a point on the sphere
    std::tuple<double, double, double> getPoint();

    // Rotates the sphere
    void rotate();
};

#endif // SPIRALSPHERE_H