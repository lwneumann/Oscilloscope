import numpy as np
from enum import Enum
import shapes

class wfMode(Enum):
    SIN = 1
    COS = 2
    SAWTOOTH = 3
    TRIANGLE = 4
    SQUARE = 5
    CONSTANT = 6


class Waveform(shapes.ParamShape):
    def __init__(self,
                 mode='SIN',
                 frequency=440,
                 amplitude=1,
                 phase=0):
        # When constant, these are the names and maps instead.
        # Named other because they hot swap with parameter_names and index_map as needed.
        self.other_name = ['Value']
        self.other_map = ['amplitude']

        super().__init__(
            modes=wfMode,
            parameter_names=['Frequency', 'Amplitude', 'Phase'],
            index_map=['frequency', 'amplitude', 'phase'],
            start_mode=mode
        )

        self.frequency = frequency
        self.amplitude = amplitude
        self.phase = phase
        return

    # ===
    def swap_maps(self):
        # Constants only use their value and nothing else so we don't display other things
        self.parameter_names, self.other_name = self.other_name, self.parameter_names
        self.index_map, self.other_map = self.other_map, self.index_map
        return

    # === Magic Methods ===
    def set_mode(self, m):
        # Switch off (skip this during initialization)
        if hasattr(self, 'mode') and self.mode.name == "CONSTANT":
            self.swap_maps()
        # Set value
        super().set_mode(m)
        # Switch on
        if self.mode.name == "CONSTANT":
            self.swap_maps()
        return

    # =====================
    # === Functionality ===
    # =====================
    def compute_buffer(self, t):
        # Get values for readability
        phase = self.phase
        amp = self.amplitude
        freq = self.frequency
        mode = self.mode.name

        # Pass variable values if they are variables
        # You cannot bind to mode
        if hasattr(phase, 'compute_buffer'):
            phase = phase.compute_buffer(t)
        if hasattr(amp, 'compute_buffer'):
            amp = amp.compute_buffer(t)
        if hasattr(freq, 'compute_buffer'):
            freq = freq.compute_buffer(t)

        # Generate the waveform
        if mode == 'SIN':
            val = amp * np.sin(2 * np.pi * freq * t + phase)
        elif mode == 'COS':
            val = amp * np.cos(2 * np.pi * freq * t + phase)
        elif mode == 'SAWTOOTH':
            val = amp * (2 * (freq * t + phase) % 2 - 1)
        elif mode == 'TRIANGLE':
            val = amp * (2 * np.abs(2 * (freq * t + phase) % 2 - 1) - 1)
        elif mode == 'SQUARE':
            val = amp * np.sign(np.sin(2 * np.pi * freq * t + phase))
        elif mode == 'CONSTANT':
            val = np.full_like(t, amp)
        else:
            raise TypeError(f"Unsupported waveform mode: {mode}")

        return val