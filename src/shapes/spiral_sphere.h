#ifndef SPIRAL_SPHERE_H
#define SPIRAL_SPHERE_H

#include <vector>

class SpiralSphere {
private:
    double theta, phi, d_theta, d_phi, r;
    double tilt_x, tilt_y, tilt_z;
    double d_tilt_x, d_tilt_y, d_tilt_z;

    const double PI = 3.141592653589793;

public:
    // Constructor
    SpiralSphere(double theta = 0, double phi = 0, double d_theta = 0.02, double d_phi = 0.001, double r = 1,
                 double tilt_x = 3.141592653589793 / 6, double tilt_y = 3.141592653589793 / 6, double tilt_z = 3.141592653589793 / 6,
                 double d_tilt_x = 0.0001, double d_tilt_y = 0, double d_tilt_z = 0);

    // Methods
    std::vector<std::vector<double>> getFrame(int num_points);
    void rotate();
};

#endif // SPIRAL_SPHERE_H