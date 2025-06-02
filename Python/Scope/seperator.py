from enum import Enum
import shape


class sMode(Enum):
    ORBIT = 1
    GRID = 2

# ==== Seperator Modes ====
class Orbit(shape.ParamShape):
    def __init__(self   ):
        super().__init__(
            parameter_names=['Orbit Radius', 'Orbit Speed', 'Phase', 'Children Size'],
            index_map=['orbit_r', 'orbit_speed', 'phase', 'children_size']
        )

        self.orbit_r = 0.5
        self.orbit_speed = 0
        self.phase = 0
        # Scale of children
        self.children_size = 0.3
        return


class Grid(shape.ParamShape):
    def __init__(self):
        super().__init__(
            parameter_names=['Grid Size', 'Buffer'],
            index_map=['grid_size', 'buffer']
        )

        # Grid size - n x n
        self.grid_size = 2
        # How much space is between each shape and the edge
        self.buffer = 0.1
        return


# ==== Actual Seperator Class ====
class Seperator(shape.Shape):
    def __init__(self, start_mode=None):
        super().__init__(
            modes=sMode,
            start_mode=start_mode
        )

        self.seperators = [
            Orbit(),
            Grid()
        ]
        return

    # ====
    def selected(self):
        return self.seperators[self.mode.value-1]

    # ==== Magic Methods ====
    # This is really just a container that points to whatever seperator is selected so it just passes
    # everything to its kids. What a good parent
    def __getitem__(self, i):
        return self.selected()[i]

    def __setitem__(self, i, v):
        self.selected()[i] = v
        return

    def __len__(self):
        return len(self.selected())

    # ==== Graphics ====
    def get_children(self):
        # Select the stored seperators children based on the mode
        return self.selected().get_children()
