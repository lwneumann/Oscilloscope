import numpy as np
from enum import Enum
from internals import shapes, collection, waveform


class pwMode(Enum):
    GEQ = 1
    LEQ = 2

class Peacewise(shapes.ParamShape):
    def __init__(self, modes=pwMode):
        super().__init__(modes,
                         parameter_names=['Divider', 'A', 'B'],
                         index_map=['divider', 'a', 'b'],
                         start_mode='GEQ')

        self.divider = 0.5
        self.a = 1
        self.b = 1
        # self.a = collection.Collection(
        #     name='A',
        #     content=waveform.Waveform(mode='CONSTANT')
        #     )
        # self.b = collection.Collection(
        #     name='B',
        #     content=waveform.Waveform(mode='CONSTANT')
        #     )
        self.name = str(self)
        return
    
    # ==== Magic Methods ====
    def __str__(self):
        symb = '>=' if self.mode.value == 1 else '<='
        return f"A {symb} B"
    
    # ====
    def set_mode(self, m):
        super().set_mode(m)
        self.name = str(self)
        return
    
    def toggle(self):
        super().toggle()
        self.name = str(self)
        return
    
    # =====================
    # === Functionality ===
    # =====================
    def compute_buffer(self, t):
        # Compute buffers for a and b
        if hasattr(self.a, 'compute_buffer'):
            a_buf = self.a.compute_buffer(t)
        else:
            a_buf = np.full_like(t, self.a, dtype=float)
        if hasattr(self.b, 'compute_buffer'):
            b_buf = self.b.compute_buffer(t)
        else:
            b_buf = np.full_like(t, self.b, dtype=float)
        # Piecewise
        if self.mode.name == 'GEQ':
            mask = t >= self.divider
        elif self.mode.name == 'LEQ':
            mask = t <= self.divider
        else:
            raise TypeError(f"Unsupported piecewise mode: {self.mode.name}")
        # Select a where mask is True, b where False
        val = np.where(mask, a_buf, b_buf)
        return val
