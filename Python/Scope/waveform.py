from enum import Enum
import sounddevice as sd
import shape

class wfMode(Enum):
    SAWTOOTH = 1
    TRIANGLE = 2
    COS = 3
    SQUARE = 4


class Waveform(shape.ParamShape):
    def __init__(self, mode='SAWTOOTH', samplerate=0, amplitude=1, phase=0):
        super().__init__(
            modes=wfMode,
            parameter_names=['Samplerate', 'Amplitude', 'Phase'],
            index_map=['samplerate', 'amplitude', 'phase'],
            start_mode=mode
        )

        self.set_mode(mode)

        self.samplerate = samplerate
        self.amplitude = amplitude
        self.phase = phase
        return
