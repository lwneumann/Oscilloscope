#ifndef WAVEGENERATOR_H
#define WAVEGENERATOR_H

#include <cmath>
#include "utils.h"

class WaveGenerator {
public:
    enum WaveType { SINE, COSINE, SQUARE, TRIANGLE, SAWTOOTH };

    WaveGenerator(WaveType type, double frequency = 1.0, double amplitude = 1.0, double phase = 0.0);

    // Generate wave value for time t
    double generate(double t);

    // Utilities
    void setFrequency(double frequency);
    void setAmplitude(double amplitude);
    void setPhase(double phase);
    void setWaveType(WaveType type);

private:
    WaveType waveType;
    double frequency;
    double amplitude;
    double phase;

    double sineWave(double t);
    double squareWave(double t);
    double triangleWave(double t);
    double sawtoothWave(double t);
};

#endif // WAVEGENERATOR_H