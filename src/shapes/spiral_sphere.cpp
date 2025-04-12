#include <iostream>
#include <cmath>
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
                 double tilt_x = M_PI / 6, double tilt_y = M_PI / 6, double tilt_z = M_PI / 6,
                 double d_tilt_x = 0.0001, double d_tilt_y = 0, double d_tilt_z = 0)
        : theta(theta), phi(phi), d_theta(d_theta), d_phi(d_phi), r(r),
          tilt_x(tilt_x), tilt_y(tilt_y), tilt_z(tilt_z),
          d_tilt_x(d_tilt_x), d_tilt_y(d_tilt_y), d_tilt_z(d_tilt_z) {}

    // Generate a buffer of points
    std::vector<std::vector<double>> getFrame(int num_points) {
        std::vector<std::vector<double>> buffer;

        for (int i = 0; i < num_points; ++i) {
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

            // Add the point to the buffer
            buffer.push_back({x_z, y_z, z_y});

            // Update angles
            theta += d_theta;
            if (theta > 2 * PI) {
                theta -= 2 * PI;
            }

            phi += d_phi;
            if (phi > PI) {
                phi = 0;
            }
        }

        return buffer;
    }

    // Rotate the sphere
    void rotate() {
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
};