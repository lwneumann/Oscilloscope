#ifndef DUPLICATE_H
# define DUPLICATE_H

#include <tuple>

class Duplicate {
public:
	enum DisplayMode { NONE, GRID, ORBIT, SPIRAL };

	Duplicate(DisplayMode mode = NONE,
		int duplicity = 2,
		double otherSetting = 0.0);

	void setMode(DisplayMode mode);
	void setDuplicity(int duplicity);
	int getDuplicity() { return duplicity; };

	std::tuple<double, double, double, double> getPoint(double t);

private:
	DisplayMode mode;
	int duplicity;
	double otherSetting;
};

#endif // DUPLICATE_H