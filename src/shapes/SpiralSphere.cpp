#include "SpiralSphere.h"
#include <cmath>
#include <tuple>

SpiralSphere::SpiralSphere(double theta_period, double phi_period, double r,
                           double tilt_x, double tilt_y, double tilt_z,
                           double d_tilt_x, double d_tilt_y, double d_tilt_z)
    : theta_period(theta_period), phi_period(phi_period), r(r),
      tilt_x(tilt_x), tilt_y(tilt_y), tilt_z(tilt_z),
      d_tilt_x(d_tilt_x), d_tilt_y(d_tilt_y), d_tilt_z(d_tilt_z) {}

std::tuple<double, double, double> SpiralSphere::getPoint(double t) {
    // Get angle
    double theta = t * theta_period;
    double phi = t * phi_period;

    // Original sphere coordinates
    double x = r * cos(theta) * sin(phi);
    double y = r * sin(theta) * sin(phi);
    double z = r * cos(phi);

    // Update angles
    if (t > ROTATE_THRESHOLD) {
        rotate();
    }

    // Return rotated point
    return utils::rotatePoint(x, y, z, tilt_x, tilt_y, tilt_z);
}

void SpiralSphere::rotate() {
    tilt_x += d_tilt_x;
    if (tilt_x > 2 * PI) {
        tilt_x -= 2 * PI;
    }
    tilt_y += d_tilt_y;
    if (tilt_y > 2 * PI) {
        tilt_y -= 2 * PI;
    }
    tilt_z += d_tilt_z;
    if (tilt_z > 2 * PI) {
        tilt_z -= 2 * PI;
    }
}