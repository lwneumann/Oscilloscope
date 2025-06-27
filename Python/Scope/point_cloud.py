from enum import Enum
import random, string
import collection, waveform, seperator, shape


# This is nearly identical to collection but is always in duplicate mode, and 
class PointCloud(shape.Shape):
    def __init__(self, name=None,
                 x=None, y=None, z=None,
                 driver=None):
        # Not using any modes just fixed a duplicate and driver
        super().__init__(
            driver=driver
            )

        # Name
        # For not just random charecters but eventually I'll add this being relevant maybe?
        # Or just remove it? But for the sake of shapes and such it is useful to have a name
        if name is None:
            self.name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        else:
            self.name = name

        # Internal Data!
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
                name='Z'
            )
            self.z.set_collapse(True)
        else:
            self.z = z

        self.seperator = seperator.Seperator(parent=self, start_mode='GRID')
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
                # Adjust index mapping if driver is present
                offset = 1 if self.driver is not None else 0
                if i[0] == 0:
                    return self.seperator[i[1:]]
                elif self.driver is not None and i[0] == 1:
                    return self.driver[i[1:]]
                elif i[0] == 1 + offset:
                    return self.x[i[1:]]
                elif i[0] == 2 + offset:
                    return self.y[i[1:]]
                elif i[0] == 3 + offset:
                    return self.z[i[1:]]
            # When its one value discard the list wrapping it
            else:
                i = i[0]
        # Now just only value needs to be indexed. Other searches have been returned
        # Index across seperator first to be consistent with visuals then get coords
        if i == 0:
            return self.seperator
        idx = 1
        if self.driver is not None:
            if i == 1:
                return self.driver
            idx += 1
        if i == idx:
            return self.x
        elif i == idx + 1:
            return self.y
        elif i == idx + 2:
            return self.z

    def __len__(self):
        # If collapsed, then just return the collpased icon else
        # return seperator, and the three dimensions, plus driver if present
        base_len = 4
        if self.driver is not None:
            base_len += 1
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
        if self.driver is None:
            children = [self.seperator, self.x, self.y, self.z]
        else:
            children = [self.seperator, self.driver, self.x, self.y, self.z]
        return children

    # =====================
    # === Functionality ===
    # =====================
    def compute_buffer(self, t):
        # For now we ignore z
        x = self.x.compute_buffer(t)
        y = self.y.compute_buffer(t)
        return x, y
