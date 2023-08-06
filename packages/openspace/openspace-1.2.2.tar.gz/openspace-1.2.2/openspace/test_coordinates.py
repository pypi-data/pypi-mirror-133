
import os
import sys

sys.path.append(os.getcwd())

from openspace.math.measurements import (
    Angle, Distance, Epoch, STANDARD_EPOCH_FMT
)
from openspace.math.linear_algebra import Vector
from openspace.math.constants import ZERO
from openspace.math.coordinates import (
    hill_to_eci,
    spherical_to_cartesian, 
    cartesian_to_spherical,
    coes_to_vector
)
from openspace.propagators import ClohessyWiltshireModel, TwoBodyModel
from openspace.math.time_conversions import get_eci_to_ecef_gst_angle
import matplotlib.pyplot as plt

def test_spherical_to_cartesian():
    r = 3643
    lat = Angle(28, "degrees").to_unit("radians")
    long = Angle(50, "degrees").to_unit("radians")
    test_input = Vector([r, lat, long])
    expected_output = Vector([2067.576, 2464.042, 1710.285])
    angle = expected_output.angle(spherical_to_cartesian(test_input))
    assert angle <= ZERO

def test_cartesian_to_spherical():
    test_input = Vector([2067.576, 2464.042, 1710.285])
    output = cartesian_to_spherical(test_input)
    r = 3643
    lat = Angle(28, "degrees").to_unit("radians")
    long = Angle(50, "degrees").to_unit("radians")

    assert abs(output.get_element(0) - r) <= 1e-3
    assert abs(output.get_element(1) - lat) <= ZERO
    assert abs(output.get_element(2) - long) <= ZERO

def test_coes_to_vector():
    conversion_factor = Distance(1, "nautical miles").to_unit("meters")
    a = 4193.935*conversion_factor
    e = 5.96096410e-2
    i = Angle(30, "degrees").to_unit("radians")
    ta = Angle(23.55315, "degrees").to_unit("radians")
    aop = Angle(50, "degrees").to_unit("radians")
    raan = Angle(40, "degrees").to_unit("radians")

    p, v = coes_to_vector(a, e, i, ta, aop, raan)

    
    expected_p = Vector([-1256.137, 3242.352, 1900.184]).scale(conversion_factor)
    expected_v = Vector([-3.675879, -1.676277, 0.6227918]).scale(conversion_factor)

    print(p)
    print(v)
    assert p.angle(expected_p) < ZERO
    assert v.angle(expected_v) < ZERO

def test_hill_to_eci():
    tgt_epoch = Epoch("Dec 25 2021 00:00:00.000", STANDARD_EPOCH_FMT)
    tgt_eci_pos = Vector([0, 42164000, 0])
    tgt_eci_vel = Vector([-3075, 0, 0])

    prop_epoch = Epoch("Dec 25 2021 00:00:00.000", STANDARD_EPOCH_FMT)
    tbm = TwoBodyModel(tgt_eci_pos, tgt_eci_vel, tgt_epoch)
    x = []
    y = []

    rel_mod_chase = ClohessyWiltshireModel(
        [0, -5000, -5000, 0, 0, 0],
        42164000
    )
    chase_r, chase_v = hill_to_eci(
        tgt_eci_pos, 
        tgt_eci_vel,
        rel_mod_chase.position,
        rel_mod_chase.velocity
    )

    rel_mod_observer = ClohessyWiltshireModel(
        [0, 10000, -140000, -.5, 0, 0],
        42164000
    )

    print(rel_mod_observer.step_to_next_tangent()/86400)
    observer_r, observer_v = hill_to_eci(
        tgt_eci_pos,
        tgt_eci_vel,
        rel_mod_observer.position,
        rel_mod_observer.velocity
    )

    r, i, c = rel_mod_observer.get_positions_over_interval(0, 86400, 600)
    plt.plot(i, r)
    plt.show()
    for t in range(0, 86400, 300):
        prop_epoch = tgt_epoch.add_seconds(t)
        gst = get_eci_to_ecef_gst_angle(prop_epoch)
        r, v = tbm.get_state_at_epoch(prop_epoch)
        r = r.rotate_about_z(gst)
        r_lat_long = cartesian_to_spherical(r)
        x.append(
            Angle(r_lat_long.get_element(2), "radians").to_unit("degrees")
        )
        y.append(r_lat_long.get_element(0)-42164000)

    plt.plot(x, y)
    plt.show()

    print(chase_r.scale(.001).get_element(0))
    print(chase_r.scale(.001).get_element(1))
    print(chase_r.scale(.001).get_element(2))
    print("")
    print(chase_v.scale(.001).get_element(0))
    print(chase_v.scale(.001).get_element(1))
    print(chase_v.scale(.001).get_element(2))
    print("")
    print(observer_r.scale(.001).get_element(0))
    print(observer_r.scale(.001).get_element(1))
    print(observer_r.scale(.001).get_element(2))
    print("")
    print(observer_v.scale(.001).get_element(0))
    print(observer_v.scale(.001).get_element(1))
    print(observer_v.scale(.001).get_element(2))
    print("")

test_hill_to_eci()