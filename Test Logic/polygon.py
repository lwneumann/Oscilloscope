"""
Generally for more than two bands.
Polygons made with points on a sphere
"""
import util, graph_path
from math import cos, sin, pi


class Polygon:
    def __init__(self, rings,
                 x_tilt=0, y_tilt=0, z_tilt=0,
                 d_x_tilt=0.1, d_y_tilt=0.001, d_z_tilt=0.005,
                 r=1):
        """
        Rings - [
                    number of points in ring
                        ⋮
                ]
        """
        self.rings = rings
        if self.rings[0] != 1:
            self.rings = [0] + self.rings
        if self.rings[-1] != 1:
            self.rings = self.rings + [0]

        self.x_tilt = x_tilt
        self.y_tilt = y_tilt
        self.z_tilt = z_tilt
        self.d_x_tilt = d_x_tilt
        self.d_y_tilt = d_y_tilt
        self.d_z_tilt = d_z_tilt

        self.r = r
        self.edges = []
        self.path = None

        self.generate()
        return
    
    def rotate(self):
        self.x_tilt += self.d_x_tilt
        if self.x_tilt > 2*pi:
            self.x_tilt -= 2*pi
        self.y_tilt += self.d_y_tilt
        if self.y_tilt > 2*pi:
            self.y_tilt -= 2*pi
        self.z_tilt += self.d_z_tilt
        if self.z_tilt > 2*pi:
            self.z_tilt -= 2*pi
        return

    def get_point(self, theta, phi):
        # Original sphere coordinates
        x = self.r * cos(theta) * sin(phi)
        y = self.r * sin(theta) * sin(phi)
        z = self.r * cos(phi)

        # Apply X-axis rotation
        y_x = y * cos(self.x_tilt) - z * sin(self.x_tilt)
        z_x = y * sin(self.x_tilt) + z * cos(self.x_tilt)

        # Apply Y-axis rotation
        x_y = x * cos(self.y_tilt) + z_x * sin(self.y_tilt)
        z_y = -x * sin(self.y_tilt) + z_x * cos(self.y_tilt)

        # Apply Z-axis rotation
        x_z = x_y * cos(self.z_tilt) - y_x * sin(self.z_tilt)
        y_z = x_y * sin(self.z_tilt) + y_x * cos(self.z_tilt)
        return x_z, y_z, z_y

    def generate_bands(self):
        step_count = len(self.rings)
        # Two ring lazy solution...
        # Doesn't make even nice looking squares and such.
        # Is ok for cylinders
        if len(self.rings) == 2:
            phi = pi/4
            step_size = pi/2
        # Otherwise start at poles
        else:
            # Starts at 0 as a step
            phi = 0
            step_size = pi/(step_count-1)
        self.points = []

        for step in range(step_count):
            # Ignore offset rings for <1 starts and ends
            if self.rings[step] != 0:
                # Start at angle offset
                theta = 0
                theta_steps = 2*pi/self.rings[step]

                # Add points
                for point in range(self.rings[step]):
                    new_p = self.get_point(theta, phi)
                    self.points.append(new_p)

                    theta += theta_steps
            phi += step_size
        return

    def get_point_i(self, r_i, p_i):
        """
        Start at zero, otherwise check all prior points and add point index
        """
        return sum([0] + [self.rings[r] for r in range(r_i)]) + p_i

    def get_nearest_point(self, point_i, other_ring_i, other_base_i):
        # [Index], Distance
        nearest_p_info = [[], None]
        for other_p in range(self.rings[other_ring_i]):
            dist = util.distance(self.points[point_i], self.points[other_base_i+other_p])
            if nearest_p_info[1] is None or dist < nearest_p_info[1]:
                nearest_p_info = [[other_base_i+other_p], dist]
            elif dist <= nearest_p_info[1]:
                nearest_p_info[0].append(other_base_i+other_p)
        return nearest_p_info[0]

    def generate_edges(self):
        # Adds edges between bands
        for ring_i in range(len(self.rings)):
            # Add wrapping bands around ring
            if self.rings[ring_i] != 1:
                base = self.get_point_i(ring_i, 0)
                self.edges += [ [ base+p, base+(p+1)%(self.rings[ring_i]) ] for p in range(self.rings[ring_i]) ]

            # Add connective rings
            if ring_i < len(self.rings)-1:
                """
                For all points in the larger ring, map one line from each point to the nearest other line
                euclid distance
                """
                larger_ring_i = ring_i if self.rings[ring_i] > self.rings[ring_i+1] else ring_i+1
                lesser_ring_i = ring_i+1 if larger_ring_i == ring_i else ring_i

                larger_p_base_i = self.get_point_i(larger_ring_i, 0)
                lesser_p_base_i = self.get_point_i(lesser_ring_i, 0)

                for point in range(self.rings[larger_ring_i]):
                    nearest_p_i = self.get_nearest_point(larger_p_base_i + point, lesser_ring_i, lesser_p_base_i)
                    for p in nearest_p_i:
                        self.edges.append([p, larger_p_base_i + point])
        return

    def generate(self):
        self.generate_bands()
        # Relations should change unless the points are changes.
        # Add a better detection later if needed
        if len(self.edges) == 0:
            self.generate_edges()
        return

    def get_point_path(self):
        # Cache path since this won't change (for now)
        if self.path is None:
            self.path = graph_path.Graph(self.edges).get_edge_covering_path(0)
        return self.path

    def generate_parameterized_path(self):
        return graph_path.parameterize_lines([self.points[i] for i in self.get_point_path()])
