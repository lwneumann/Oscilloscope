#include "LineSphere.h"
#include <cmath>
#include <tuple>

LineSphere::LineSphere(int x_bands, int y_bands, double r,
                           double tilt_x, double tilt_y, double tilt_z,
                           double d_tilt_x, double d_tilt_y, double d_tilt_z)
    : x_bands(x_bands), y_bands(y_bands), r(r),
      tilt_x(tilt_x), tilt_y(tilt_y), tilt_z(tilt_z),
      d_tilt_x(d_tilt_x), d_tilt_y(d_tilt_y), d_tilt_z(d_tilt_z),
      total_bands(x_bands + y_bands), band_size(1/total_bands) {}

std::tuple<double, double, double> LineSphere::getPoint(double t) {
    // Get Band
    int band = t * total_bands;
    double internal_t = (t - (band_size * band)) / band_size;

    // Get angle
    double theta, phi;
    if (band < x_bands) {
        theta = 2 * PI * band / x_bands;
        phi = PI * internal_t;
    } else {
        theta = 2 * PI * internal_t;
        phi = PI * band / x_bands;
    }

    // Original sphere coordinates
    double x = r * cos(theta) * sin(phi);
    double y = r * sin(theta) * sin(phi);
    double z = r * cos(phi);

    // Apply X-axis rotation
    double y_x = y * cos(tilt_x) - z * sin(tilt_x);
    double z_x = y * sin(tilt_x) + z * cos(tilt_x);

    // Apply Y-axis rotation
    double x_y = x * cos(tilt_y) + z_x * sin(tilt_y);
    double z_y = -x * sin(tilt_y) + z_x * cos(tilt_y);

    // Apply Z-axis rotation
    double x_z = x_y * cos(tilt_z) - y_x * sin(tilt_z);
    double y_z = x_y * sin(tilt_z) + y_x * cos(tilt_z);

    // Update angles
    if (t > ROTATE_THRESHOLD) {
        rotate();
    }

    return std::make_tuple(x_z, y_z, z_y);
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