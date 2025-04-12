#include <iostream>
#include <portaudio.h>
#include "audio_data.h"
#include "audio_callback.h"
#include "generators.h"

int main() {
    // Initialize PortAudio
    Pa_Initialize();

    // Audio data for the callback
    AudioData data;
    // Start absolute time
    data.time = 0.0f;
    // Base frequency (1 Hz)
    data.frequency = 1.0f;
    // Set initial generator to sawtooth
    data.tGenerator = sawtooth;

    // Open output stream
    PaStream* stream;
    Pa_OpenDefaultStream(&stream,
                         // Input channels
                         0,
                         // Stero Output
                         2,
                         // 32-bit floating point audio
                         paFloat32,
                         // Sample rate
                         SAMPLE_RATE,
                         // Frames per buffer
                         FRAMES_PER_BUFFER,
                         // Callback function
                         audioCallback,
                         // Points to render
                         &data
    );

    // Start the stream
    Pa_StartStream(stream);

    // Wait for user input to stop
    std::cout << "Playing audio. Press Enter to stop." << std::endl;
    std::cin.get();

    // Stop the stream
    Pa_StopStream(stream);
    Pa_CloseStream(stream);
    // Terminate PortAudio
    Pa_Terminate();

    return 0;
}
