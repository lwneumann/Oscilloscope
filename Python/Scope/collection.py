from enum import Enum
import random, string
import waveform, seperator, shape


class cMode(Enum):
    PLUS = 1
    TIMES = 2
    DUPLICATE = 3


class Collection(shape.Shape):
    def __init__(self, name=None, content=None, mode='PLUS'):
        # Get shape methods to ensure no crashes later from unused methods in Collection
        super().__init__(modes=cMode)
        
        # Name
        # For not just random charecters but eventually I'll add this being relevant maybe?
        # Or just remove it? But for the sake of shapes and such it is useful to have a name

        if name is None:
            self.name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        else:
            self.name = name

        # Mode
        self.set_mode(mode)
        
        # Collection
        self.collection = content
        if content is None:
            self.collection = [waveform.Waveform()]

        self.seperator = None
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
            if self.seperator is not None and i == 0:
                return self.seperator
            return self.collection[i]
    
    def __len__(self):
        # Length of internal collection + seperator if valid
        return len(self.collection) + (self.seperator is not None)

    # ==== Change Settings ====
    def add(self, other):
        self.collection.append(other)
        return

    # ==== Graphics ====
    def get_children(self):
        if self.seperator is None:
            return self.collection
        else:
            return [self.seperator.name].extend(self.collection)
