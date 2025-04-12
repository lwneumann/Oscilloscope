#include <cmath>
#include "generators.h"

float sawtooth(float time, float frequency) {
    // Wraps time * frequency to [0, 1]
    return fmod(time * frequency, 1.0f);
}

float sineWave(float time, float frequency) {
    // Scaled to [0, 1]
    return 0.5f * (std::sin(2.0f * M_PI * frequency * time) + 1.0f);
}
