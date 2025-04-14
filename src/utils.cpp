#include "utils.h"
#include <cmath>


namespace utils {
    int sgn(double value) {
        return (value > 0) - (value < 0);
    }

    double to_square_wave(double t, double period) {
        return sgn(std::sin((2 * PI * t) / period));
    }
}