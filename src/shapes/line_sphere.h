#ifndef LINE_SPHERE_H
#define LINE_SPHERE_H

#include <vector>

class LineSphere {
private:
    int x_lines, y_lines;
    double r, tilt_x, tilt_y, tilt_z;
    double d_tilt_x, d_tilt_y, d_tilt_z;

    const double PI = 3.141592653589793;

public:
    // Constructor
    LineSphere(double r = 1, double tilt_x = 3.141592653589793 / 6, double tilt_y = 3.141592653589793 / 6, double tilt_z = 3.141592653589793 / 6,
               double d_tilt_x = 0.5, double d_tilt_y = 0.1, double d_tilt_z = 0,
               int x_lines = 10, int y_lines = 10);

    // Methods
    std::vector<double> getPoint(double theta, double phi);
    std::vector<std::vector<double>> getFrame(int line_points = 50);
    void rotate();
};

#endif // LINE_SPHERE_H