#include <iostream>
#include <cmath>
#include <vector>

class LineSphere {
private:
    int x_lines, y_lines;
    double r, tilt_x, tilt_y, tilt_z;
    double d_tilt_x, d_tilt_y, d_tilt_z;

    const double PI = 3.141592653589793;

public:
    LineSphere(double r = 1, double tilt_x = M_PI / 6, double tilt_y = M_PI / 6, double tilt_z = M_PI / 6,
               double d_tilt_x = 0.5, double d_tilt_y = 0.1, double d_tilt_z = 0,
               int x_lines = 10, int y_lines = 10)
        : r(r), tilt_x(tilt_x), tilt_y(tilt_y), tilt_z(tilt_z),
          d_tilt_x(d_tilt_x), d_tilt_y(d_tilt_y), d_tilt_z(d_tilt_z),
          x_lines(x_lines), y_lines(y_lines) {}

    std::vector<double> getPoint(double theta, double phi) {
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

        return {x_z, y_z, z_y};
    }

    std::vector<std::vector<double>> getFrame(int line_points = 50) {
        std::vector<std::vector<double>> frame;

        for (int x_l = 0; x_l < x_lines; ++x_l) {
            double theta = 2 * PI * x_l / x_lines;
            for (int point = 0; point < line_points; ++point) {
                double phi = PI * point / (line_points - 1);
                frame.push_back(getPoint(theta, phi));
            }
        }

        for (int y_l = 0; y_l < y_lines; ++y_l) {
            double phi = PI * y_l / y_lines;
            for (int point = 0; point < line_points; ++point) {
                double theta = 2 * PI * point / (line_points - 1);
                frame.push_back(getPoint(theta, phi));
            }
        }

        return frame;
    }

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