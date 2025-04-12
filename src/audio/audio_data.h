#ifndef AUDIO_DATA_H
#define AUDIO_DATA_H

#include <functional>

// Constants
#define SAMPLE_RATE 44100
#define FRAMES_PER_BUFFER 256

// Structure to hold audio data and generator
struct AudioData {
    // Absolute time
    float time;
    // Frequency of the waveform
    float frequency;
    // Function to generate t
    std::function<float(float, float)> tGenerator;
};

#endif // AUDIO_DATA_H