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
        super().__init__(modes=wfMode, parameter_names=['Samplerate', 'Amplitude', 'Phase'])

        self.samplerate = samplerate
        self.amplitude = amplitude
        self.phase = phase
        return

    # ==== Magic Methods ====    
    def __getitem__(self, i):
        if isinstance(i, list) and len(i) == 1:
            i = i[0]

        if i >= len(self) or i < 0:
            raise IndexError(f"Waveform index {i} is out of range")
        elif i == 0:
            return self.samplerate
        elif i == 1:
            return self.amplitude
        elif i == 2:
            return self.phase

    def __setitem__(self, i, v):
        if isinstance(i, list) and len(i) == 1:
            i = i[0]

        if i >= len(self) or i < 0:
            raise IndexError(f"Waveform index {i} is out of range")
        elif i == 0:
            self.samplerate = v
        elif i == 1:
            self.amplitude = v
        elif i == 2:
            self.phase = v
        return