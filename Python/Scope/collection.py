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

        self.seperator = seperator.Seperator()
        return

    # ==== 
    def is_seperating(self):
        # Duplicator mode is 3
        # (See cMode)
        return self.mode.value == 3
    
    # ===== Magic Methods ====
    def __str__(self):
        mode_chr = ['+', 'x', 'D'][self.mode.value-1]
        return f"{mode_chr}: {self.name}"
    
    def __repr__(self):
        return str(self)

    def __getitem__(self, i):
        if i >= len(self) or i < 0:
            raise IndexError(f"Collection index {i} is out of range")
        
        # Sometimes you get passed a list of indices which need to sink through the tree
        if isinstance(i, list):
            # If the list is just one thing then just grab that thing.
            if len(i) == 1:
                return self.collection[i[0]]
            # Otherwise pass the remaining indices down the tree
            else:
                return self.collection[i[0]][i[1:]]
        # If there is just one value index accordingly
        else:
            # If in seperator mode, allow indexing that
            if self.is_seperating() and i == 0:
                return self.seperator
            # Otherwise index as normal
            else:
                # Shift the index back by one to account for the seperator when being used.
                return self.collection[i if not self.is_seperating() else i-1]

    def __len__(self):
        # Length of internal collection + seperator if valid
        return len(self.collection) + self.is_seperating()
    

    # ==== Change Settings ====
    def add(self, other):
        self.collection.append(other)
        return

    # ==== Graphics ====
    def get_children(self):
        if self.is_seperating():
            return [self.seperator] + self.collection
        else:
            return self.collection
