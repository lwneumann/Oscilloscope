from math import ceil
import shapes
import numpy as np


def divide_time(chunk_count, t):
    """
    Divide t into chunk_count unique, equal-length chunks.
    If t is a 2D array (shape [3, N]), split each axis into unique chunks.
    Returns a list of chunked arrays for each axis.
    """
    # If t is a list/array of 3 arrays (x, y, z)
    if isinstance(t, (list, tuple)) and len(t) == 3 and hasattr(t[0], '__len__'):
        # Split each axis into unique chunks
        return [divide_time(chunk_count, t[i]) for i in range(3)]
    else:
        # t is a 1D array
        t = np.asarray(t)
        chunk_sizes = [len(t) // chunk_count + (1 if i < len(t) % chunk_count else 0) for i in range(chunk_count)]
        indices = np.cumsum([0] + chunk_sizes)
        chunks = [t[indices[i]:indices[i+1]] for i in range(chunk_count)]
        return chunks


def rotate_points(x, y, z, tilt_x, tilt_y, tilt_z):
        """
        Rotate points with a given tilt
        when calling this make sure to update internal tilt
        """
        y_x = y * np.cos(tilt_x) - z * np.sin(tilt_x)
        z_x = y * np.sin(tilt_x) + z * np.cos(tilt_x)
        x_y = x * np.cos(tilt_y) + z_x * np.sin(tilt_y)
        z_y = -x * np.sin(tilt_y) + z_x * np.cos(tilt_y)
        x_z = x_y * np.cos(tilt_z) - y_x * np.sin(tilt_z)
        y_z = x_y * np.sin(tilt_z) + y_x * np.cos(tilt_z)
        return [x_z, y_z, z_y]


# === Classes ===
class Rotator(shapes.ParamShape):
    def __init__(self, modes=None, collapsed=True):
        super().__init__(
            modes,
            collapsed=collapsed,
            parameter_names=['dx', 'dy', 'dz', 'Tilt x', 'Tilt y', 'Tilt z'],
            index_map=['dx', 'dy', 'dz', 'tilt_x', 'tilt_y', 'tilt_z']
        )

        self.dx = 0
        self.dy = 0
        self.dz = 0
        self.tilt_x = 0
        self.tilt_y = 0
        self.tilt_z = 0
        return

    def rotate_points(self, x, y, z):
        rotated_points = rotate_points(x, y, z, self.tilt_x, self.tilt_y, self.tilt_z)
        
        # Update spin
        self.tilt_x += self.dx
        self.tilt_y += self.dy
        self.tilt_z += self.dz

        return rotated_points