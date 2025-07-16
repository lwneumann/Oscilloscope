"""
There are many instances you want to display multiple shapes at once not just combine the outputs.
This displays multipl children by allocating normalized _t_ across the kids.

Modes:
 - Grid:
    A grid of children. Debating how to deal with multiple different kids
 - Orbit
    Ring/orbit of chilren

More to come probably.
"""
import numpy as np
from enum import Enum
import shapes
import utils


class sMode(Enum):
    ORBIT = 1
    GRID = 2

# ==== Seperator Modes ====
class Orbit(shapes.ParamShape):
    def __init__(self):
        super().__init__(
            parameter_names=['Orbit Radius', 'Orbit Speed', 'Phase', 'Children Size'],
            index_map=['orbit_r', 'orbit_speed', 'phase', 'children_size']
        )

        self.orbit_r = 0.5
        self.orbit_speed = 0
        self.phase = 0
        # Scale of children
        self.children_size = 0.3
        # TODO add orientation / upright vs ring around the center
        return


class Grid(shapes.ParamShape):
    def __init__(self):
        super().__init__(
            parameter_names=['Grid Size', 'Edge Buffer', 'Rescale'],
            index_map=['grid_size', 'edge_buffer', 'rescale']
        )

        # Grid size - n x n
        self.grid_size = 1
        # How much space is between each shape and the edge
        self.edge_buffer = 0.5
        # Rescale children to the grid size
        self.rescale = 1
        return

    # === Functionality ===
    def seperate_children(self, child_buffers):
        return child_buffers

    def duplicate_buffer(self, buffer):
        # Ensure legal grid size
        if self.grid_size < 1:
            self.grid_size = 1
        # Get Grid
        n = self.grid_size
        if n == 1:
            return buffer
        # Rescale
        if self.rescale:
            buffer[0] *= 1/n
            buffer[1] *= 1/n
            buffer[2] *= 1/n

        # buffer: [x, y, z], each is a 1D array
        # Split each axis into n*n segments
        chunks = utils.divide_time(n * n, buffer)
        grid_step = (2 - 2 * self.edge_buffer) / (n - 1)
        
        # Shift chunks
        for r in range(n):
            for c in range(n):
                # Get shift (for now this is just a grid on the xy plane)
                x_shift = self.edge_buffer + c * grid_step - 1
                y_shift = self.edge_buffer + r * grid_step - 1
                
                # Get chunk index and shift the x, y
                idx = r * n + c

                chunks[0][idx] += x_shift
                chunks[1][idx] += y_shift
        
        # Recombine shifted chunks
        x = np.concatenate(chunks[0])
        y = np.concatenate(chunks[1])
        z = np.concatenate(chunks[2])
        shifted_buffer = np.stack([x, y, z], axis=0)
        return shifted_buffer


# ==== Actual Seperator Class ====
class Seperator(shapes.Shape):
    def __init__(self, parent, start_mode=None):
        super().__init__(
            modes=sMode,
            start_mode=start_mode
        )

        # Grid size and so on need to know how many children there are in order to dynamically adjust accodingly
        self.parent = parent

        # List of all types of seperators for the collection
        self.seperators = [
            Orbit(),
            Grid()
        ]
        return

    # ====
    def selected(self):
        # Get the selected seperator
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
        base_len = 1
        # If not collapsed actually get len
        if not self.collapsed:
            base_len = len(self.selected())
        return base_len

    # ==== Graphics ====
    def get_children(self):
        # Select the stored seperators children based on the mode
        return self.selected().get_children()

    # =====================
    # === Functionality ===
    # =====================
    def seperate_children(self, child_buffers):
        # Let the selected duplicator seperate the children accordingly
        return self.selected().seperate_children(child_buffers)

    def duplicate_child(self, buffer):
        # Duplicate buffer
        return self.selected().duplicate_buffer(buffer)
