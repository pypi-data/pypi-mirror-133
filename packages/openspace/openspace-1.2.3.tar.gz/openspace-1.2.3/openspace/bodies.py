from openspace.math.measurements import Epoch, Distance
from openspace.math.time_conversions import J2000_JULIAN_DATE
from math import sin, radians, degrees, cos
from openspace.math.linear_algebra import Vector

class WGS84:
    def __init__(self):
        self.equatorial_radius = 6378137
        self.flattening = 1/298.257223563
        self.angular_rate = 72.92115e-6
        self.mu = 3986004.418e8

class Earth:
    def __init__(self, geodetic_model=WGS84()):
        self.equatorial_radius = geodetic_model.equatorial_radius
        self.flattening = geodetic_model.flattening
        self.angular_rate = geodetic_model.angular_rate
        self.mu = geodetic_model.mu

class Sun:
    def __init__(self):
        self.equatorial_raidus = 695700
        self.flattening = .00005
        self.mu = 1.32712440018e20

    def get_position(self, epoch: Epoch):
        n = epoch.to_julian_date() - J2000_JULIAN_DATE
        L = 280.460 + .9856474*n
        g = 357.528 + .9856003*n
        sin_g = sin(radians(g))
        sin_2g = sin(2*radians(g))
        cos_g = cos(radians(g))
        cos_2g = cos(2*radians(g))
        lam = L + 1.915*sin_g + .02*sin_2g
        eps = 23.436 - .0000004*n
        R = 1.00014 - .01671*cos_g - .00014*cos_2g
        r = Distance(R, "astronomical units").to_unit("meters")
        x = r*cos(radians(lam))
        y = r*cos(radians(eps))*sin(radians(lam))
        z = r*sin(radians(eps))*sin(radians(lam))

        return Vector([x, y, z])

class Moon:
    def __init__(self):
        self.equatorial_radius = 1738.1
        self.flattening = .0012
        self.mu = 4.9048695e12

    def get_position(self, epoch: Epoch):
        n = epoch.to_julian_date() - J2000_JULIAN_DATE
        n/=36525
