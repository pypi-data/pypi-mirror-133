from openspace.propagators import ClohessyWiltshireModel, TwoBodyModel
from openspace.math.linear_algebra import Vector
from openspace.math.measurements import Epoch
from openspace.math.coordinates import vector_to_coes
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time

def test():
    rel_mod = ClohessyWiltshireModel([0, -200000, 0, 1, 0, 1], 42164000)
    x, y, z = [], [], []
    for t in range(0, 86400*2, 300):
        state = rel_mod.solve_next_state(t)
        burn_mod = ClohessyWiltshireModel(state, 42164000)
        for t2 in range(300, 86400, 300):
            burn = burn_mod.solve_waypoint_burn(t2, Vector([0, 0, 0]))
            x.append(t)
            y.append(t2)
            #burn = Vector(burn[0:2])
            if burn.magnitude() < 50:
                z.append(burn.magnitude())
            else:
                z.append(50)

    data = pd.DataFrame(data={'x':x, 'y':y, 'z':z})
    data = data.pivot(index='y', columns='x', values='z')
    ax = sns.heatmap(data, cbar_kws={'label': 'Burn Magnitude (m/s)'})
    ax.invert_yaxis()
    ax.set_xlabel("Time Past Initial Epoch (s)")
    ax.set_ylabel("Time to Intercept (s)")
    ax.set_title('Threat Delta-V')
    plt.show()

def run():
    test()
