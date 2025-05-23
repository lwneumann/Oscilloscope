#include "waveGenerator.h"

WaveGenerator::WaveGenerator(WaveType type,
        double frequency, double amplitude,
        double phase,
        double wave_speed, double sample_rate)
    : waveType(type),
        frequency(frequency), amplitude(amplitude),
        phase(phase), wave_speed(wave_speed), sample_rate(sample_rate)
    {}

double WaveGenerator::generate(double t) {
    // Normalize t to [0, 1] with phase
    t = std::fmod(t + phase, 1.0);
    switch (waveType) {
        case SINE: return sineWave(t);
        // Useful for circles and such without manually setting offset
        case COSINE: return sineWave(t + 0.25);
        case SQUARE: return squareWave(t);
        case TRIANGLE: return triangleWave(t);
        case SAWTOOTH: return sawtoothWave(t);
        default: return 0.0;
    }
    // Step wave
    phase += wave_speed / sample_rate;
}

void WaveGenerator::setFrequency(double frequency) { this->frequency = frequency; }
void WaveGenerator::setAmplitude(double amplitude) { this->amplitude = amplitude; }
void WaveGenerator::setPhase(double phase) { this->phase = phase; }
void WaveGenerator::setWaveSpeed(double wave_speed) { this->phase = wave_speed; }
void WaveGenerator::setSampleRate(double sample_rate) { this->sample_rate = sample_rate; }
void WaveGenerator::setWaveType(WaveType type) { this->waveType = type; }

double WaveGenerator::sineWave(double t) {
    return amplitude * std::sin(2 * PI * frequency * t);
}

double WaveGenerator::squareWave(double t) {
    return amplitude * (t < 0.5 ? 1.0 : -1.0);
}

double WaveGenerator::triangleWave(double t) {
    return amplitude * (t < 0.5 ? 4 * t - 1 : 3 - 4 * t);
}

double WaveGenerator::sawtoothWave(double t) {
    return amplitude * (2 * t - 1);
}
