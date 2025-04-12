#include <iostream>
#include <portaudio.h>
#include "audio_data.h"
#include "audio_callback.h"
#include "generators.h"
#include "shapes/shape_collection.h"
#include "shapes/spiral_sphere.cpp"

int main() {
    // Initialize ShapeCollection
    ShapeCollection shapeCollection;

    // Create a SpiralSphere instance
    SpiralSphere spiralSphere;

    // Create a Shape instance that wraps the SpiralSphere
    Shape spiralSphereShape = {
        [&spiralSphere](int num_points) { return spiralSphere.getFrame(num_points); }, // getFrame function
        1.0,    // scale
        0.0,    // x offset
        0.0,    // y offset
        1000    // number of points per frame
    };

    // Add the adapted SpiralSphere to the ShapeCollection
    shapeCollection.addShape(spiralSphereShape);

    // Demonstrate points from the SpiralSphere
    std::cout << "Spiral Sphere Points from ShapeCollection:" << std::endl;
    for (int i = 0; i < 5; ++i) {
        std::vector<double> point = shapeCollection.popPoint();
        std::cout << "Point " << i << ": (" << point[0] << ", " << point[1] << ", " << point[2] << ")" << std::endl;
    }

    // Initialize PortAudio
    Pa_Initialize();

    // Audio data for the callback
    AudioData data;
    data.time = 0.0f;
    data.frequency = 1.0f;
    data.tGenerator = sawtooth;

    // Open output stream
    PaStream* stream;
    Pa_OpenDefaultStream(&stream,
                         0, // No input channels
                         2, // Stereo output
                         paFloat32,
                         SAMPLE_RATE,
                         FRAMES_PER_BUFFER,
                         audioCallback,
                         &data);

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