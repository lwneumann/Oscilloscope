from enum import Enum
from shape import Shape
import sounddevice as sd


class wfMode(Enum):
    SAWTOOTH = 1
    TRIANGLE = 2
    COS = 3
    SQUARE = 4


class Waveform(Shape):
    def __init__(self, mode='SAWTOOTH', samplerate=0, amplitude=1, offset=0):
        super().__init__()

        self.set_mode(mode)
        self.samplerate = samplerate
        self.amplitude = amplitude
        self.offset = offset

        self.parameter_names = ['Samplerate', 'Amplitude', 'Offset']
        return

    # ==== Magic Methods ====
    def __str__(self):
        return self.mode.name

    def __repr__(self):
        return str(self)
    
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
            return self.offset

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
            self.offset = v
        return

    def __len__(self):
        # 3 Parameters! We love magic numbers.
        # Mode is like name.
        return 3

    # ==== Change Settings ====
    def toggle(self):
        # Cycle through modes
        modes = list(wfMode)
        self.mode = modes[(self.mode.value)%len(modes)]
        return

    def set_mode(self, m):
        # Set mode explicitly
        if m in [wf.name for wf in list(wfMode)]:
            self.mode = wfMode[m]
        elif m in [wf.value for wf in list(wfMode)]:
            self.mode = wfMode(m)
        else:
            raise KeyError(f"{m} is not a valid wfMode key")
        return

    # ==== Graphics ====
    def get_children(self):
        return self.parameter_names