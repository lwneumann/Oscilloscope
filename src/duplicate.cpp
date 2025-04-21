#include "duplicate.h"
#include "cmath"
#include <tuple>


Duplicate::Duplicate(DisplayMode mode, int duplicity)
	: mode(mode), duplicity(duplicity)
	{}

void Duplicate::setMode(DisplayMode mode) { this->mode = mode; }
void Duplicate::setDuplicity(int duplicity) { this->duplicity = duplicity; }

std::tuple<double, double, double> Duplicate::getPoint(double t) {
	return std::make_tuple(t, t, t);
}