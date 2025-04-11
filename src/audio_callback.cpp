#include "audio_callback.h"

int audioCallback(const void* inputBuffer, void* outputBuffer,
                  unsigned long framesPerBuffer,
                  const PaStreamCallbackTimeInfo* timeInfo,
                  PaStreamCallbackFlags statusFlags,
                  void* userData) {
    AudioData* data = static_cast<AudioData*>(userData);
    float* out = static_cast<float*>(outputBuffer);

    for (unsigned int i = 0; i < framesPerBuffer; ++i) {
        // Generate t using the current generator function
        float t = data->tGenerator(data->time, data->frequency);
        data->time += 1.0f / SAMPLE_RATE; // Increment absolute time

        // Generate x and y coordinates based on the square pattern
        float x, y;
        generateSquarePattern(t, x, y);

        // Map x and y to audio output for left and right channels
        // Left channel: Scale x to range -1 to 1
        *out++ = x * 2.0f - 1.0f;
        // Right channel: Scale y to range -1 to 1
        *out++ = y * 2.0f - 1.0f;
    }

    return paContinue;
}