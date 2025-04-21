#ifndef DUPLICATE_H
# define DUPLICATE_H

#include <tuple>

class Duplicate {
public:
	enum DisplayMode { GRID, ORBIT, SPIRAL };

	Duplicate(DisplayMode mode,
		int duplicity = 2);

	void setMode(DisplayMode mode);
	void setDuplicity(int duplicity);

	std::tuple<double, double, double> getPoint(double t);

private:
	DisplayMode mode;
	int duplicity;
}

#endif // DUPLICATE_H