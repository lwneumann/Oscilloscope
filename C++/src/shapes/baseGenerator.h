#ifndef BASE_GENERATOR_H
#define BASE_GENERATOR_H

#include <tuple>

class BaseGenerator {
public:
    virtual ~BaseGenerator() = default;

    virtual std::tuple<double, double, double> getPoint(double t) = 0;
};

#endif // BASE_GENERATOR_H