from math import cos, sin, pi


"""
Create points looping around a sphere with custom speed on both angles and all axis of tilt on the sphere
"""
class SpiralSphere:
    def __init__(self, theta=0, phi=0, d_theta=0.02, d_phi=0.001, r=1,
                 tilt_x=pi / 6, tilt_y=pi / 6, tilt_z=pi / 6,
                 d_tilt_x=0.0001, d_tilt_y=0, d_tilt_z=0):
        self.theta = theta
        self.d_theta = d_theta
        
        self.phi = phi
        self.d_phi = d_phi
        
        self.r = r
        self.bounds = [r, r, r]
        
        self.tilt_x = tilt_x
        self.tilt_y = tilt_y
        self.tilt_z = tilt_z

        self.d_tilt_x = d_tilt_x
        self.d_tilt_y = d_tilt_y
        self.d_tilt_z = d_tilt_z
        return

    def get_point(self):
        # Original sphere coordinates
        x = self.r * cos(self.theta) * sin(self.phi)
        y = self.r * sin(self.theta) * sin(self.phi)
        z = self.r * cos(self.phi)

        # Apply X-axis rotation
        y_x = y * cos(self.tilt_x) - z * sin(self.tilt_x)
        z_x = y * sin(self.tilt_x) + z * cos(self.tilt_x)

        # Apply Y-axis rotation
        x_y = x * cos(self.tilt_y) + z_x * sin(self.tilt_y)
        z_y = -x * sin(self.tilt_y) + z_x * cos(self.tilt_y)

        # Apply Z-axis rotation
        x_z = x_y * cos(self.tilt_z) - y_x * sin(self.tilt_z)
        y_z = x_y * sin(self.tilt_z) + y_x * cos(self.tilt_z)

        # Update angles
        self.theta += self.d_theta
        if self.theta > 2 * pi:
            self.theta -= 2 * pi

        self.phi += self.d_phi
        if self.phi > pi:
            self.phi = 0

        return [(x_z, y_z, z_y)]

    def rotate(self):
        self.tilt_x += self.d_tilt_x
        if self.tilt_x > 2*pi:
            self.tilt_x -= 2*pi
        self.tilt_y += self.d_tilt_y
        if self.tilt_y > 2*pi:
            self.tilt_y -= 2*pi
        self.tilt_z += self.d_tilt_z
        if self.tilt_z > 2*pi:
            self.tilt_z -= 2*pi
        return


"""
Sphere with bands
"""
class LineSphere:
    def __init__(self, r=1,
                 tilt_x=pi / 6, tilt_y=pi / 6, tilt_z=pi / 6,
                 d_tilt_x=0.5, d_tilt_y=0.1, d_tilt_z=0,
                 x_lines=10, y_lines=10):
        self.x_lines = x_lines
        self.y_lines = y_lines
        
        self.r = r
        self.bounds = [r, r, r]
        
        self.tilt_x = tilt_x
        self.tilt_y = tilt_y
        self.tilt_z = tilt_z

        self.d_tilt_x = d_tilt_x
        self.d_tilt_y = d_tilt_y
        self.d_tilt_z = d_tilt_z
        return

    def get_point(self, theta, phi):
        # Original sphere coordinates
        x = self.r * cos(theta) * sin(phi)
        y = self.r * sin(theta) * sin(phi)
        z = self.r * cos(phi)

        # Apply X-axis rotation
        y_x = y * cos(self.tilt_x) - z * sin(self.tilt_x)
        z_x = y * sin(self.tilt_x) + z * cos(self.tilt_x)

        # Apply Y-axis rotation
        x_y = x * cos(self.tilt_y) + z_x * sin(self.tilt_y)
        z_y = -x * sin(self.tilt_y) + z_x * cos(self.tilt_y)

        # Apply Z-axis rotation
        x_z = x_y * cos(self.tilt_z) - y_x * sin(self.tilt_z)
        y_z = x_y * sin(self.tilt_z) + y_x * cos(self.tilt_z)

        return [(x_z, y_z, z_y)]

    def get_frame(self, line_points=50):
        frame = []

        for x_l in range(self.x_lines):
            theta = 2 * pi * x_l / self.x_lines
            for point in range(line_points):
                phi = pi * point / (line_points - 1)
                frame += self.get_point(theta, phi)

        for y_l in range(self.y_lines):
            phi = pi * y_l / self.y_lines
            for point in range(line_points):
                theta = 2 * pi * point / (line_points - 1)
                frame += self.get_point(theta, phi)

        return frame

    def rotate(self):
        self.tilt_x += self.d_tilt_x
        if self.tilt_x > 2*pi:
            self.tilt_x -= 2*pi
        self.tilt_y += self.d_tilt_y
        if self.tilt_y > 2*pi:
            self.tilt_y -= 2*pi
        self.tilt_z += self.d_tilt_z
        if self.tilt_z > 2*pi:
            self.tilt_z -= 2*pi
        return
