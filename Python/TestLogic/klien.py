from math import cos, sin, pi


class KleinBottle:
    def __init__(self, u=0, v=0, d_u=0.5, d_v=0.05, r=3,
                 tilt_x=pi/6, tilt_y=pi/6, tilt_z=pi/6,
                 d_tilt_x=0.0001, d_tilt_y=0, d_tilt_z=0):
        self.u = u
        self.d_u = d_u
        
        self.v = v
        self.d_v = d_v
        
        self.r = r
        self.bounds = []
        
        self.tilt_x = tilt_x
        self.tilt_y = tilt_y
        self.tilt_z = tilt_z

        self.d_tilt_x = d_tilt_x
        self.d_tilt_y = d_tilt_y
        self.d_tilt_z = d_tilt_z
        return

    def get_point(self):
        # Klein bottle parametric equations
        x = (self.r + cos(self.u / 2) * sin(self.v) - sin(self.u / 2) * sin(2 * self.v)) * cos(self.u)
        y = (self.r + cos(self.u / 2) * sin(self.v) - sin(self.u / 2) * sin(2 * self.v)) * sin(self.u)
        z = sin(self.u / 2) * sin(self.v) + cos(self.u / 2) * sin(2 * self.v)

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
        self.u += self.d_u
        if self.u > 2 * pi:
            self.u -= 2 * pi

        self.v += self.d_v
        if self.v > 2 * pi:
            self.v -= 2 * pi

        return [(x_z, y_z, z_y)]

    def rotate(self):
        self.tilt_x += self.d_tilt_x
        if self.tilt_x > 2 * pi:
            self.tilt_x -= 2 * pi
        self.tilt_y += self.d_tilt_y
        if self.tilt_y > 2 * pi:
            self.tilt_y -= 2 * pi
        self.tilt_z += self.d_tilt_z
        if self.tilt_z > 2 * pi:
            self.tilt_z -= 2 * pi
        return
