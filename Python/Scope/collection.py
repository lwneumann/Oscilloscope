from enum import Enum
from shape import Shape
import random, string
import waveform


class cMode(Enum):
    PLUS = 1
    TIMES = 2
    DUPLICATE = 3


class Collection(Shape):
    def __init__(self, name=None, content=None, mode='PLUS'):
        super().__init__()
        
        if name is None:
            self.name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        else:
            self.name = name

        self.set_mode(mode)
        
        self.collection = content
        if content is None:
            self.collection = [waveform.Waveform()]
        return

    # ===== Magic Methods ====
    def __str__(self):
        mode_chr = ['+', 'x', 'D'][self.mode.value-1]
        return f"{mode_chr}: {self.name}"
    
    def __repr__(self):
        return str(self)

    def __getitem__(self, i):
        if i >= len(self) or i < 0:
            raise IndexError(f"Collection index {i} is out of range")
        
        if isinstance(i, list):
            if len(i) == 1:
                return self.collection[i[0]]
            else:
                return self.collection[i[0]][i[1:]]
        else:
            return self.collection[i]
    
    def __len__(self):
        return len(self.collection)

    # ==== Change Settings ====
    def toggle(self):
        # Cycle through modes
        modes = list(cMode)
        self.mode = modes[(self.mode.value)%len(modes)]
        return

    def add(self, other):
        self.collection.append(other)
        return

    def set_mode(self, m):
        # Set mode explicitly
        if m in [wf.name for wf in list(cMode)]:
            self.mode = cMode[m]
        elif m in [wf.value for wf in list(cMode)]:
            self.mode = cMode(m)
        else:
            raise KeyError(f"{m} is not a valid cMode key")
        return

    # ==== Graphics ====
    def get_children(self):
        return self.collection
