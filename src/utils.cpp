#include "utils.h"
#include <cmath>


double to_square_wave(double t, bool full_range) {
	double square_t = std::floor(2 * t);
	if (full_range) {
		square_t = 2 * (square_t - 0.5);
	}
	return square_t;
}