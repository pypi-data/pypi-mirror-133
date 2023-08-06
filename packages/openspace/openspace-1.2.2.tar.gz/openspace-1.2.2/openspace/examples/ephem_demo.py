import matplotlib.pyplot as plt
from openspace.propagators import (
    ClohessyWiltshireModel, 
    TwoBodyModel, 
    TwoBodyEphemeris
)
from openspace.math.linear_algebra import Vector
from openspace.math.measurements import Epoch, STANDARD_EPOCH_FMT
from openspace.math.time_conversions import SECONDS_IN_DAY, SECONDS_IN_HOUR

#Arbitrarily defined ECI vector for target
START_EPOCH = Epoch("Dec 25 2021 00:00:00.000", STANDARD_EPOCH_FMT)
TARGET_ECI_POS = Vector([42159500, 0, 0])
TARGET_ECI_VEL = Vector([0, 3075, 0])

#Relative state desired for observer vehicle
cw_observer = ClohessyWiltshireModel(
    [0, 10000, -140000, -.5, 0, 0],
    42164000
)

#Relative state desired for chase vehicle
cw_chase = ClohessyWiltshireModel(
     [-5000, 0, -5000, 0, 0, 0],
    42164000
)

#Creation of TwoBodyModels for all vehicles
target_tbm = TwoBodyModel(TARGET_ECI_POS, TARGET_ECI_VEL, START_EPOCH)
observer_tbm = TwoBodyModel.from_two_body_and_cw_model(target_tbm, cw_observer)
chase_tbm = TwoBodyModel.from_two_body_and_cw_model(target_tbm, cw_chase)

#Synchronizing epochs to be one full period in the past (just for added visuals)
target_period = target_tbm.get_period()
t = -target_period
target_tbm.step_to_epoch(START_EPOCH.add_seconds(t), True)
observer_tbm.step_to_epoch(START_EPOCH.add_seconds(t), True)
chase_tbm.step_to_epoch(START_EPOCH.add_seconds(t), True)

#Creating ephemeris objects for all vehicles
target_ephem = TwoBodyEphemeris.from_two_body_model(target_tbm)
observer_ephem = TwoBodyEphemeris.from_two_body_model(observer_tbm)
chase_ephem = TwoBodyEphemeris.from_two_body_model(chase_tbm)

#Defining maneuvers for target vehicle (one occurs)
dv_times = [
    3*SECONDS_IN_HOUR+target_period, #This occurs 3 hours from START_EPOCH
    5.5*SECONDS_IN_HOUR+target_period #This occurs 5.5 hours from START_EPOCH
]
dv_list = [
    Vector([1, 0, 0]), #1 m/s all radial
    Vector([0, 1, 0])  #1 m/s all in-track
]

#This generates a full set of ephemeris with or without burns with step size
#of 300 seconds for two full periods
target_ephem.generate_ephemeris(target_period*2, 300, dv_times, dv_list)
chase_ephem.generate_ephemeris(target_period*2, 300)
observer_ephem.generate_ephemeris(target_period*2, 300)

#This plots data from the ephemeris objects
plt.plot(target_ephem.longitudes, target_ephem.altitudes, "r-")
plt.plot(chase_ephem.longitudes, chase_ephem.altitudes, "b-")
plt.plot(observer_ephem.longitudes, observer_ephem.altitudes, "g-")
plt.scatter(target_ephem.burn_longitudes, target_ephem.burn_altitudes, c="y")
plt.show()

#This outputs stk formatted ephem files
target_ephem.write_ephem_to_file('target_ephem.e')
chase_ephem.write_ephem_to_file('chase_ephem.e')
observer_ephem.write_ephem_to_file('observer_ephem.e')