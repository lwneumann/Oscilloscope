from enum import Enum
import shape


# 
class sMode(Enum):
    ORBIT = 1
    GRID = 1

# ==== Seperator Modes ====
class Orbit(shape.ParamShape):
    def __init__(self, modes=None, parameter_names=['Orbit Radius', 'Orbit Speed', 'Phase', 'Children Size']):
        super().__init__(modes, parameter_names)
        
        self.orbit_r = 0.5
        self.orbit_speed = 0
        self.phase = 0
        # Scale of children
        self.children_size = 0.3
        return

    # ==== Magic Methods ====
    def __getitem__(self, i):
        if isinstance(i, list) and len(i) == 1:
            i = i[0]

        if i >= len(self) or i < 0:
            raise IndexError(f"Orbit index {i} is out of range")
        elif i == 0:
            return self.orbit_r
        elif i == 1:
            return self.orbit_speed
        elif i == 2:
            return self.phase
        elif i == 3:
            return self.children_size
        return

    def __setitem__(self, i, v):
        if isinstance(i, list) and len(i) == 1:
            i = i[0]

        if i >= len(self) or i < 0:
            raise IndexError(f"Orbit index {i} is out of range")
        elif i == 0:
            self.orbit_r = v
        elif i == 1:
            self.orbit_speed = v
        elif i == 2:
            self.phase = v
        elif i == 3:
            self.children_size = v
        return


class Grid(shape.ParamShape):
    def __init__(self, modes=None, parameter_names=['Grid Size', 'Buffer']):
        super().__init__(modes, parameter_names)

        # Grid size - n x n
        self.grid_size = 2
        # How much space is between each shape and the edge
        self.buffer = 0.1
        return


# ==== Actual Seperator Class ====
class Seperator(shape.Shape):
    def __init__(self):
        super.__init__(modes=sMode)

        self.set_mode()
        return

    # ==== Magic Methods ====
    def __str__(self):
        return self.mode.name

    # ==== Graphics ====
    def get_children(self):
        return self.mode.get_children()