#include "LineSphere.h"
#include <cmath>
#include <tuple>

LineSphere::LineSphere(int x_bands, int y_bands, double r,
                           double tilt_x, double tilt_y, double tilt_z,
                           double d_tilt_x, double d_tilt_y, double d_tilt_z)
    : x_bands(x_bands), y_bands(y_bands), r(r),
      tilt_x(tilt_x), tilt_y(tilt_y), tilt_z(tilt_z),
      d_tilt_x(d_tilt_x), d_tilt_y(d_tilt_y), d_tilt_z(d_tilt_z),
      total_bands(x_bands + y_bands), band_size(1.0 / total_bands) {}

std::tuple<double, double, double> LineSphere::getPoint(double t) {
    // Get Band
    int band = t * total_bands;
    double internal_t = (t - (band_size * band)) / band_size;

    // Get angle
    double theta, phi;
    if (band < x_bands) {
        theta = 2 * PI * band / x_bands;
        phi = 2 * PI * internal_t;
    } else {
        theta = 2 * PI * internal_t;
        phi = 2 * PI * band / x_bands;
    }

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

void LineSphere::rotate() {
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