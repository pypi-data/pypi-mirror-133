from openspace.propagators import TwoBodyModel
from openspace.math.measurements import Epoch
from openspace.math.linear_algebra import Vector
from random import gauss, uniform
from math import degrees, radians

class Observation:

    def __init__(self, epoch, observer_position, observed_vector):
        self.epoch = Epoch.from_timestamp(epoch.timestamp)
        self.observer_position = Vector(observer_position)
        self.observed_vector = Vector(observed_vector)

    def get_cross_line_of_sight_error(self, two_body_model):
        r, _ = two_body_model.get_state_at_epoch(self.epoch)
        target_vec = r.minus(self.observer_position).scale(.001)
        return target_vec.angle(self.observed_vector)*target_vec.magnitude()

class SpaceBasedOptical:

    def __init__(self, two_body_model, three_sigma_noise):
        self.two_body_model = TwoBodyModel(
            two_body_model.r0,
            two_body_model.v0,
            two_body_model.epoch0
        )

        self.noise = three_sigma_noise/3

    def get_simulated_observation(self, two_body_model:TwoBodyModel):
        self.two_body_model.step_to_epoch(two_body_model.epoch0)
        target_vec = self.two_body_model.get_target_vector(two_body_model)
        sun_vec = self.two_body_model.get_sun_vector()
        axis = target_vec.cross(sun_vec)
        ang = gauss(0, self.noise)
        ob_noise_1d = target_vec.rotate_about_axis(axis, ang)
        ang = radians(uniform(0, 360))
        return Observation(
            two_body_model.epoch0,
            self.two_body_model.r0,
            ob_noise_1d.rotate_about_axis(target_vec, ang)
        )
