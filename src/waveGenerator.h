#ifndef WAVEGENERATOR_H
#define WAVEGENERATOR_H

#include <cmath>
#include "utils.h"

class WaveGenerator {
public:
    enum WaveType { SINE, COSINE, SQUARE, TRIANGLE, SAWTOOTH };

    WaveGenerator(WaveType type,
        double frequency = 1.0, double amplitude = 1.0,
        double phase = 0.0,
        double wave_speed = 64.0, double sample_rate = 44100.0);

    // Generate wave value for time t
    double generate(double t);

    // Utilities
    void setFrequency(double frequency);
    void setAmplitude(double amplitude);
    void setPhase(double phase);
    void setWaveSpeed(double wave_speed);
    void setSampleRate(double sample_rate);
    void setWaveType(WaveType type);

    // Debugging utilities
    WaveType getWaveType() const { return waveType; }
    double getFrequency() const { return frequency; }
    double getAmplitude() const { return amplitude; }
    double getPhase() const { return phase; }
    double getWaveSpeed() const { return wave_speed; }
    double getSampleRate() const { return sample_rate; }
    std::string getWaveTypeAsString() const;

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