#include <iostream>
#include <cmath>
#include <portaudio.h>
#include <array>
#include "shapes/allShapes.h"
#include "utils.h"
#include "duplicate.h"


const double SAMPLE_RATE = 44100.0;
// const double SAMPLE_RATE = 48000.0;
const int FRAMES_PER_BUFFER = 256;
const double WAVE_SPEED = 64.0;


// Audio callback function
static int audioCallback(const void *inputBuffer, void *outputBuffer,
                         unsigned long framesPerBuffer,
                         const PaStreamCallbackTimeInfo* timeInfo,
                         PaStreamCallbackFlags statusFlags,
                         void *generatorData, void duplicatorData) {
    
    auto* generator = static_cast<BaseGenerator*>(generatorData);
    
    Duplicate duplicator = Duplicate(Duplicate::ORBIT, 2);
    

    float* out = static_cast<float*>(outputBuffer);
    static double phase = 0.0;

    for (unsigned int i = 0; i < framesPerBuffer; i++) {
        // Get step
        double t = std::fmod(phase, 1.0);
        
        // Get duplicate info
        auto duplicate_info = duplicator.getPoint(t);
        double local_t = std::get<0>(duplicate_info);
        double x_offset = std::get<1>(duplicate_info);
        double y_offset = std::get<2>(duplicate_info);
        // double z_offset = std::get<3>(duplicate_info);
        // Get point
        auto point = generator->getPoint(local_t);
        double x = std::get<0>(point);
        double y = std::get<1>(point);
        if (duplicator.getDuplicity() != 1) {
            x *= 0.7/duplicator.getDuplicity();
            y *= 0.7/duplicator.getDuplicity();
            x += x_offset;
            y += y_offset;
            // std::cout << x_offset << std::endl;
        }
        // Apply projection eventually if wanted maybe

        // Output
        // -- Left channel
        *out++ = static_cast<float>(x);
        // -- Right channel
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
    SpiralSphere generator = SpiralSphere();
    // LineSphere generator = LineSphere();
    // mushroom generator = mushroom();

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