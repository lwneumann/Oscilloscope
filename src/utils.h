#ifndef UTILS_H
#define UTILS_H

// Define constants
#ifndef PI
#define PI 3.14159265358979323846
#endif

#ifndef ROTATE_THRESHOLD
#define ROTATE_THRESHOLD 0.9
#endif

// Later add lerp, distance and some other functions to a utils.cpp
namespace utils {
	int sgn(double value);
	double to_square_wave(double t, double period = 1);
}


#endif // MATH_UTILS_H