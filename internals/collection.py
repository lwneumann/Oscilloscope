import copy
import random, string
import numpy as np
from enum import Enum
from math import ceil
from internals import waveform, seperator, shapes, utils


class cdMode(Enum):
    TIMES = 1
    PLUS = 2
    DUPLICATE = 3

class cMode(Enum):
    TIMES = 1
    PLUS = 2


class Collection(shapes.Shape):
    def __init__(self, name=None,
                 start_mode=None,
                 content=None,
                 start_seperator=None,
                 collapsed=False,
                 can_duplicate=False):
        # Get shape methods to ensure no crashes later from unused methods in Collection
        super().__init__(
            modes= cdMode if can_duplicate else cMode,
            start_mode=start_mode,
            collapsed=collapsed
        )

        # Name
        # For not just random charecters but eventually I'll add this being relevant maybe?
        # Or just remove it? But for the sake of shapes and such it is useful to have a name
        if name is None:
            self.name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        else:
            self.name = name

        self.mode_labels = ['x', '+', 'D']

        # Collection of other shapes and components
        if isinstance(content, list):
            self.collection = content
        elif content is None:
            self.collection = [waveform.Waveform()]
        else:
            self.collection = [content]

        self.seperator = start_seperator
        if start_seperator is None:
            self.seperator = seperator.Seperator(parent=self, start_mode='GRID')
        return

    # ==== 
    def is_seperating(self):
        # Duplicator mode is 3
        # (See cMode)
        return self.mode.name == "DUPLICATE"
    
    # ===== Magic Methods ====
    def __str__(self):
        mode_chr = self.mode_labels[self.mode.value-1]
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
                # Shift the index back to account for the seperator when being used.
                return self.collection[i if not self.is_seperating() else i-1]

    def __setitem__(self, i, v):
        """
        Only allow setitem for the collection itself not parameters for now
        """
        # Seperator is index 0 so only allow [self.is_seperating(), len(self)]
        if self.is_seperating() < i >= len(self):
            raise IndexError(f"{self.__class__.__name__} index {i} is out of range")

        self.collection[i - self.is_seperating()] = v
        return

    def __len__(self):
        # If collapsed, then just return the collpased icon else
        # Length of seperator + internal collection
        base_len = 1
        if not self.collapsed:
            base_len = self.is_seperating() + len(self.collection)
        return base_len

    # TODO fix this :)
    # Need to add deepcopy everywhere
    # def __deepcopy__(self, memo):
    #     copied_collection = copy.deepcopy(self.collection, memo)
    #     copied_seperator = copy.deepcopy(self.seperator, memo)
    #     return Collection(
    #         name=self.name,
    #         start_mode=self.mode.value,
    #         content=copied_collection,
    #         start_seperator=copied_seperator
    #     )

    # ==== Change Settings ====
    def append(self, other):
        self.collection.append(other)
        return

    def set_all_collapse(self, c):
        # Sets the collapse of all of its children
        self.seperator.set_collapse(c)
        for child in self.collection:
            if hasattr(child, "set_all_collapse"):
                child.set_all_collapse(c)
            child.set_collapse(c)
        self.set_collapse(c)
        return

    def pop(self, i):
        # Reverse indexing
        n = len(self.collection)
        if i < 0:
            i = n + i
        assert 0 <= i < n, f"{self.__class__.__name__} index {i} is out of range for pop (size {n})"
        return self.collection.pop(i)

    # ==== Graphics ====
    def get_children(self):
        if self.is_seperating():
            return [self.seperator] + self.collection
        else:
            return self.collection

    # =====================
    # === Functionality ===
    # =====================
    def compute_buffer(self, t):
        if self.mode.name in ["PLUS", "TIMES"]:
            # Compute each child's buffer
            child_buffers = [child.compute_buffer(t) for child in self.collection]

            # Stack buffers to shape (num_children, 3)
            stacked = np.stack(child_buffers, axis=0)

            if self.mode.name == 'PLUS':
                # Sum across children for each dimension
                buffer = np.sum(stacked, axis=0)
            elif self.mode.name == 'TIMES':
                # Product across children for each dimension
                buffer = np.prod(stacked, axis=0)
        # Duplicate across children
        elif self.mode.name == "DUPLICATE":
            children_chunks = utils.divide_time(len(self.collection), t)
            buffers = [child.compute_buffer(children_chunks[i]) for i, child in enumerate(self.collection)]
            buffer = self.seperator.seperate_children(buffers)
        return buffer
