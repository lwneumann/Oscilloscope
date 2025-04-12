#ifndef LINESPHERE_H
#define LINESPHERE_H

#include "utils.h"
#include <tuple>

class LineSphere {
private:
    int x_bands, y_bands;
    double r;
    double tilt_x, tilt_y, tilt_z;
    double d_tilt_x, d_tilt_y, d_tilt_z;
    int total_bands;
    double band_size;

public:
    LineSphere(int x_bands = 8, int y_bands = 8, double r = 1,
                 double tilt_x = PI / 6, double tilt_y = PI / 6, double tilt_z = PI / 6,
                 double d_tilt_x = 0.0001, double d_tilt_y = 0, double d_tilt_z = 0);

    std::tuple<double, double, double> getPoint(double t);
    void rotate();
};

#endif // LINESPHERE_H