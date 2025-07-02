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
                 period=None,
                 amplitude=1,
                 phase=0):
        super().__init__(
            modes=wfMode,
            parameter_names=['Frequency', 'Period', 'Amplitude', 'Phase'],
            index_map=['frequency', 'period', 'amplitude', 'phase'],
            start_mode=mode
        )

        self.frequency = frequency
        self.period = period if period is not None else 1/frequency
        self.amplitude = amplitude
        self.phase = phase
        return

    def __setitem__(self, i, v):
        # Updates chained variables if needed by definition:
        # period = 1/frequency and frequency = 1/period
        selected_index = self._index_map[i]
        if selected_index in ['period', 'frequency']:
            # Prevent illegal input
            if v == 0:
                return
            # Update other value
            other_index = self._index_map.index('period' if selected_index=='frequency' else 'frequency')
            super().__setitem__(other_index, 1/v)
        # Update value
        super().__setitem__(i, v)
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