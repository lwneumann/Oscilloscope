import numpy as np
from enum import Enum
from math import sin, cos
import random, string
from internals import utils, collection, waveform, seperator, shapes


# This is nearly identical to collection but is always in duplicate mode, and 
class PointCloud(shapes.Shape):
    def __init__(self, name=None,
                 x=None, y=None, z=None):
        # Not using any modes just fixed a duplicate
        super().__init__()

        # Name
        # For not just random charecters but eventually I'll add this being relevant maybe?
        # Or just remove it? But for the sake of shapes and such it is useful to have a name
        if name is None:
            self.name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        else:
            self.name = name

        # --- Internal Data ---
        self.seperator = seperator.Seperator(parent=self, start_mode='GRID')
        
        self.rotator = utils.Rotator()

        # x
        if x is None:
            self.x = collection.Collection(
                name='X',
                content=[waveform.Waveform(
                        mode='COS'
                    )]
            )
        else:
            self.x = x
        # y
        if y is None:
            self.y = collection.Collection(
                name='Y'
            )
        else:
            self.y = y
        # z
        if z is None:
            self.z = collection.Collection(
                name='Z',
                content=[waveform.Waveform(
                        mode='CONSTANT',
                        amplitude=0
                    )]
            )
        else:
            self.z = z
        return
    
    # ===== Magic Methods ====
    def __str__(self):
        return f"*: {self.name}"
    
    def __repr__(self):
        return str(self)

    def __getitem__(self, i):
        if i >= len(self) or i < 0:
            raise IndexError(f"PointCloud index {i} is out of range")
        
        # Sometimes you get passed a list of indices which need to sink through the tree
        if isinstance(i, list):
            # If its a longer list pass that 'down' the tree
            if len(i) != 1:
                if i[0] == 0:
                    return self.seperator[i[1:]]
                elif i[0] == 1:
                    return self.rotator[i[1:]]
                elif i[0] == 2:
                    return self.x[i[1:]]
                elif i[0] == 3:
                    return self.y[i[1:]]
                elif i[0] == 4:
                    return self.z[i[1:]]
            # When its one value discard the list wrapping it
            else:
                i = i[0]
        # Now just only value needs to be indexed. Other searches have been returned
        # Index across seperator first to be consistent with visuals then get coords
        if i == 0:
            return self.seperator
        elif i == 1:
            return self.rotator
        if i == 2 :
            return self.x
        elif i == 3 :
            return self.y
        elif i == 4 :
            return self.z


    def __len__(self):
        # If collapsed, then just return the collpased icon else
        # Seperator, rotator, x, y, z is the 5
        base_len = 5
        return 1 if self.collapsed else base_len

    # ==== Change Settings ====
    def add(self, other):
        self.collection.append(other)
        return

    def set_all_collapse(self, c):
        # Sets the collapse of all of its children
        self.seperator.set_collapse(c)
        self.x.set_all_collapse(c)
        self.y.set_all_collapse(c)
        self.z.set_all_collapse(c)
        self.set_collapse(c)
        return

    # ==== Graphics ====
    def get_children(self):
        # Return appropriate values
        return [self.seperator, self.rotator, self.x, self.y, self.z]

    # =====================
    # === Functionality ===
    # =====================
    def compute_buffer(self, t):
        # Get points
        x = self.x.compute_buffer(t)
        y = self.y.compute_buffer(t)
        z = self.z.compute_buffer(t)
        # Rotate points
        rotated_buffer = self.rotator.rotate_points(x, y, z)
        # Apply seperator
        return self.seperator.duplicate_child(rotated_buffer)
