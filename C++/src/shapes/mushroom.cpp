#include "mushroom.h"
#include <cmath>
#include <tuple>

mushroom::mushroom(double theta_period, double phi_period,
                        double r, double cap_r,
                        double wiggle, double d_wiggle,
                        double tilt_x, double tilt_y, double tilt_z,
                        double d_tilt_x, double d_tilt_y, double d_tilt_z)
    : theta_period(theta_period), phi_period(phi_period),
        r(r), cap_r(cap_r),
        wiggle(wiggle), d_wiggle(d_wiggle),
        tilt_x(tilt_x), tilt_y(tilt_y), tilt_z(tilt_z),
        d_tilt_x(d_tilt_x), d_tilt_y(d_tilt_y), d_tilt_z(d_tilt_z) {}

std::tuple<double, double, double> mushroom::getPoint(double t) {
    // Get angle
    double theta = t * theta_period;

    // Radius check
    double radius;
    if (t < 0.75) {
        radius = r;
    } else {
        radius = sin(2*PI*t) * cap_r;
    }

    // Get points
    double x = cos(theta) * radius;
    double y = 2.0 * t - 1;
    double z = sin(theta) * radius;

    // Add wiggle
    x += (t/4.0) * cos(2 * PI * wiggle + 4.0*t);
    z += (t/4.0) * sin(2 * PI * wiggle + 4.0*t);

    wiggle += d_wiggle;
    if (wiggle > 1) {
        wiggle = 0;
    }

    // Update angles
    if (t > ROTATE_THRESHOLD) {
        rotate();
    }

    // Return rotated point
    return utils::rotatePoint(x, y, z, tilt_x, tilt_y, tilt_z);
}

void mushroom::rotate() {
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