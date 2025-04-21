#include "duplicate.h"
#include "utils.h"
#include "cmath"
#include <tuple>
#include <iostream>


Duplicate::Duplicate(DisplayMode mode, int duplicity, double otherSetting)
	: mode(mode), duplicity(duplicity), otherSetting(otherSetting)
	{}

void Duplicate::setMode(DisplayMode mode) { this->mode = mode; }
void Duplicate::setDuplicity(int duplicity) { this->duplicity = duplicity; }

std::tuple<double, double, double, double> Duplicate::getPoint(double t) {
	double x = 0.0; double y = 0.0; double z = 0.0;
	double local_t = t;

	switch (mode) {
        case GRID: {
        	if (duplicity != 1) {
	        	// duplicity x duplicity grid
	        	local_t = duplicity*duplicity * t;
	        	// Grid info
	        	// Grid scale adds an imaginary buffer around the edges
	        	double grid_scale = otherSetting * 2.0 / (duplicity-1);
	        	int grid_x = std::fmod(local_t, duplicity);
	        	int grid_y = local_t / duplicity;
	        	// Normalize t
	        	local_t = std::fmod(local_t, 1.0);
	        	// Get grid pos centered around [0, 0]
	        	x = grid_x * grid_scale - otherSetting;
	        	y = grid_y * grid_scale - otherSetting;
        	}
        	break;
        }
        case ORBIT: {
        	double theta_step = (2.0 * PI) / duplicity;
        	local_t = duplicity * t;
        	int duplicity_i = local_t;
        	local_t = std::fmod(local_t, 1.0);
        	x = 2.0 * cos((duplicity_i * theta_step) + otherSetting) / 3.0;
        	y = 2.0 * sin((duplicity_i * theta_step) + otherSetting) / 3.0;
        	
        	otherSetting += 0.001;
        	if (otherSetting >= 2*PI) {
        		otherSetting -= 2*PI;
        	}
        	// std::cout << otherSetting << std::endl;
        	break;
        }
        case SPIRAL:
        	break;
        default:
        	break;
    }

	return std::make_tuple(local_t, x, y, z);
}