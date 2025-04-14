#include <iostream>
#include <cmath>
#include <portaudio.h>
#include "SpiralSphere.h"
#include "LineSphere.h"
#include "mushroom.h"
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

    float* out = static_cast<float*>(outputBuffer);
    static double phase = 0.0;

    for (unsigned int i = 0; i < framesPerBuffer; i++) {
        // Get step
        double t = std::fmod(phase, 1.0);
    
        // x, y - SpiralSphere
        // auto point = generator->getPoint(t);
        // double x = std::get<0>(point);
        // double y = std::get<1>(point);
        // double x = cos(2*PI*t);
        // double y = sin(2*PI*t);
        // double x = (t/4.0) * sin(4 * PI * t);
        // double y = 2.0*t-1;

        // Square wave for duping
        double x = utils::to_square_wave(t);
        double y = 0;

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
    mushroom generator;

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