#include <iostream>
#include <cmath>
#include <portaudio.h>
#include <array>
#include "shapes/SpiralSphere.h"
#include "shapes/LineSphere.h"
#include "shapes/mushroom.h"
#include "utils.h"

const double SAMPLE_RATE = 44100.0;
const int FRAMES_PER_BUFFER = 256;
const double WAVE_SPEED = 64.0;
// 64

// Audio callback function
static int audioCallback(const void *inputBuffer, void *outputBuffer,
                         unsigned long framesPerBuffer,
                         const PaStreamCallbackTimeInfo* timeInfo,
                         PaStreamCallbackFlags statusFlags,
                         void *userData) {
    
    // SpiralSphere* generator = static_cast<SpiralSphere*>(userData);
    // LineSphere* generator = static_cast<LineSphere*>(userData);
    // mushroom* generator = static_cast<mushroom*>(userData);

    std::array<SpiralSphere, 3> generator = {
        *static_cast<SpiralSphere*>(userData),
        *static_cast<SpiralSphere*>(userData),
        *static_cast<SpiralSphere*>(userData)
    };

    float* out = static_cast<float*>(outputBuffer);
    static double phase = 0.0;

    for (unsigned int i = 0; i < framesPerBuffer; i++) {
        // Get step
        double t = std::fmod(phase, 1.0);
    
        // x, y
        // double x, y;
        // x = y = 0;
        // auto point = generator->getPoint(std::fmod(6.0*t, 1.0));
        // auto point = generator->getPoint(std::fmod(t, 1.0));
        // double x = std::get<0>(point);
        // double y = std::get<1>(point);

        // Get each sphere
        // x = 0.45*x + 0.55 * utils::to_square_wave(t, 0.5) * utils::to_square_wave(t + 0.5);
        // y = 0.45*y + 0.55 * utils::to_square_wave(t, 0.5);
        double local_t = generator.size * t;
        double sphere_i = floor(local_t);
        local_t = std::fmod(local_t, 1.0);

        // Left channel
        *out++ = static_cast<float>(x);
        // Right channel
        *out++ = static_cast<float>(y);

        // Step sawtooth
        phase += WAVE_SPEED / SAMPLE_RATE;
    }

    return paContinue;
}

int main() {
    PaError err = Pa_Initialize();
    if (err != paNoError) {
        std::cerr << "PortAudio error: " << Pa_GetErrorText(err) << std::endl;
        return 1;
    }

    // Create generators
    // SpiralSphere generator;
    // LineSphere generator;
    // mushroom generator;

    std::array<SpiralSphere, 3> generator;

    PaStream* stream;
    err = Pa_OpenDefaultStream(&stream,
                               // Input channels
                               0,
                               // Stereo output
                               2,
                               // 32-bit floating point output
                               paFloat32,
                               SAMPLE_RATE,
                               FRAMES_PER_BUFFER,
                               audioCallback,
                               // Sphere for points
                               &generator);

    if (err != paNoError) {
        std::cerr << "PortAudio error: " << Pa_GetErrorText(err) << std::endl;
        Pa_Terminate();
        return 1;
    }

    err = Pa_StartStream(stream);
    if (err != paNoError) {
        std::cerr << "PortAudio error: " << Pa_GetErrorText(err) << std::endl;
        Pa_Terminate();
        return 1;
    }

    std::cout << "Press Enter to stop..." << std::endl;
    std::cin.get();

    err = Pa_StopStream(stream);
    if (err != paNoError) {
        std::cerr << "PortAudio error: " << Pa_GetErrorText(err) << std::endl;
    }

    err = Pa_CloseStream(stream);
    if (err != paNoError) {
        std::cerr << "PortAudio error: " << Pa_GetErrorText(err) << std::endl;
    }

    Pa_Terminate();
    return 0;
}