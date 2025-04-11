#ifndef AUDIO_CALLBACK_H
#define AUDIO_CALLBACK_H

#include <portaudio.h>
#include "audio_data.h"
#include "parametric_functions.h"

// Audio callback function prototype
int audioCallback(const void* inputBuffer, void* outputBuffer,
                  unsigned long framesPerBuffer,
                  const PaStreamCallbackTimeInfo* timeInfo,
                  PaStreamCallbackFlags statusFlags,
                  void* userData);

#endif // AUDIO_CALLBACK_H