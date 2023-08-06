from openspace.math.coordinates import (
	vector_to_coes, cartesian_to_spherical, hill_to_eci, eci_to_hill
)
import numpy as np
from math import degrees, sqrt, sin, cos, pi, acos, atan2, tan, isnan, atan
from openspace.bodies import Earth, Sun
from openspace.math.linear_algebra import Matrix, Vector
from openspace.math.constants import ZERO, GEO_RADIUS
from openspace.math.measurements import Epoch, Distance, Angle
from openspace.configs.formats import STANDARD_EPOCH_FMT, STK_EPOCH_FMT
from openspace.math.time_conversions import get_eci_to_ecef_gst_angle
import pkg_resources

class TwoBodyModel:
	def __init__(self, r0, v0, epoch:Epoch):
		self.r0 = Vector(r0)
		self.v0 = Vector(v0)
		
		self.epoch0 = Epoch(
			epoch.to_string_format(STANDARD_EPOCH_FMT),
			STANDARD_EPOCH_FMT
		)

		self.ephem_start_epoch = Epoch(
			epoch.to_string_format(STANDARD_EPOCH_FMT),
			STANDARD_EPOCH_FMT
		)
		

	@classmethod
	def from_two_body_and_cw_model(self, two_body_model, cw_model):
		r, v = two_body_model.get_eci_state_from_cw_model(cw_model)
		return self(r, v, two_body_model.epoch0)

	def get_range_to_two_body_model(self, two_body_model):
		r, v = two_body_model.get_state_at_epoch(self.epoch0)
		return self.r0.distance(r)
		
	def step_to_epoch(self, epoch, reset_ephem_start_epoch=False):
		self.r0, self.v0 = self.get_state_at_epoch(epoch)
		self.epoch0 = epoch
		if reset_ephem_start_epoch:
			self.ephem_start_epoch = epoch

	def maneuver_at_epoch(self, epoch, ric_burn):
		self.step_to_epoch(epoch)
		a, _, _, _, _, _ = vector_to_coes(self.r0, self.v0)
		cw_model = ClohessyWiltshireModel([0,0,0,0,0,0], a)
		cw_model.apply_velocity_change(ric_burn)
		self.r0, self.v0 = self.get_eci_state_from_cw_model(cw_model)

	def get_geo_altitude(self):
		radius = Distance(self.r0.magnitude(), "meters").to_unit("kilometers")
		return radius - GEO_RADIUS.to_unit("kilometers")

	def get_sun_vector(self):
		return Sun().get_position(self.epoch0)

	def get_target_vector(self, two_body_model):
		r, _ = two_body_model.get_state_at_epoch(self.epoch0)
		return r.minus(self.r0)

	def get_sun_sat_target_angle(self, two_body_model):
		sun_vec = self.get_sun_vector()
		target_vec = self.get_target_vector(two_body_model)
		return degrees(sun_vec.angle(target_vec))

	def get_earth_sat_target_angle(self, two_body_model):
		earth_vec = self.r0.scale(-1)
		target_vec = self.get_target_vector(two_body_model)
		return degrees(earth_vec.angle(target_vec))

	def get_longitude(self):
		gst = get_eci_to_ecef_gst_angle(self.epoch0)
		r = self.r0.rotate_about_z(gst)
		r_lat_long = cartesian_to_spherical(r)
		long = Angle(r_lat_long.get_element(2), "radians").to_unit("degrees")
		return long

	def get_ephem_line(self):
		t = self.epoch0.get_time_delta(self.ephem_start_epoch).total_seconds()
		line = " ".join(
			[
				str(t), 
				str(self.r0.get_element(0)),
				str(self.r0.get_element(1)),
				str(self.r0.get_element(2)),
				str(self.v0.get_element(0)),
				str(self.v0.get_element(1)),
				str(self.v0.get_element(2)),
				"\n"
			]
		)
		return line

	def get_eci_state_from_cw_model(self, cw_model):
		r, v = hill_to_eci(
			self.r0, 
			self.v0, 
			cw_model.position, 
			cw_model.velocity
		)

		return r, v

	def get_cw_model_from_eci_state(self, two_body_model):
		pos, vel = two_body_model.get_state_at_epoch(self.epoch0)
		r, v = eci_to_hill(self.r0, self.v0, pos, vel)
		state = [
			r.get_element(0),
			r.get_element(1),
			r.get_element(2),
			v.get_element(0),
			v.get_element(1),
			v.get_element(2)
		]

		a, _, _, _, _, _ = vector_to_coes(self.r0, self.v0)
		return ClohessyWiltshireModel(state, a)

	def get_state_at_epoch(self, epoch):
		ea = self.get_current_eccentric_anomaly()

		period = self.get_period()
		n = 2*pi/period

		dt = epoch.get_time_delta(self.epoch0)
		m0 = self.get_current_mean_anomaly()
		m = m0 + n*(dt.total_seconds())
		ea = self.solve_eccentric_anomaly(m)

		_, e, _, ta0, _, _ = vector_to_coes(self.r0, self.v0)

		ta = atan2(tan(ea/2), sqrt((1-e)/(1+e)))*2

		dta = ta - ta0
		if abs(dta) < ZERO:
			return self.r0, self.v0
		elif dta < 0:
			dta+=2*pi

		mu = Earth().mu
		r0 = self.r0.magnitude()
		h = self.r0.cross(self.v0).magnitude()
		
		vr0 = self.r0.dot(self.v0)/r0
		r = h**2/(mu*(1 + (h**2/mu/r0 - 1)*cos(dta) - h*vr0/mu*sin(dta)))

		f = 1 - ((mu*r)/h**2)*(1 - cos(dta))
		g = r*r0*sin(dta)/h

		f_dot = mu*(1-cos(dta))*(mu*(1-cos(dta))/h**2-(1/r0)-(1/r))/h/sin(dta)
		g_dot = 1 - mu*r0*(1-cos(dta))/h**2

		r1 = self.r0.scale(f).plus(self.v0.scale(g))
		v1 = self.r0.scale(f_dot).plus(self.v0.scale(g_dot))

		return r1, v1

	def solve_eccentric_anomaly(self, ma):
		_, e, _, _, _, _ = vector_to_coes(self.r0, self.v0)
		ea = ma
		converged = False
		guess = ma + e*sin(ea)
		while not converged:
			ea = ma + e*sin(guess)
			if abs(ea - guess) < ZERO:
				converged = True
			else:
				guess = ea

		return ea


	def get_period(self):
		a, _, _, _, _, _ = vector_to_coes(self.r0, self.v0)
		return 2*pi*sqrt(a**3/Earth().mu)

	def get_current_mean_anomaly(self):
		ea = self.get_current_eccentric_anomaly()
		_, e, _, _, _, _ = vector_to_coes(self.r0, self.v0)
		return ea - e*sin(ea)

	def get_current_eccentric_anomaly(self):
		_, e, _, ta, _, _ = vector_to_coes(self.r0, self.v0)
		ea = atan2(sqrt(1-e**2)*sin(ta), (e+cos(ta)))

		return ea

	def get_perigee_radius(self):
		a, e, _, _, _, _ = vector_to_coes(self.r0, self.v0)
		rp = a*(1-e)
		return rp

	def get_apogee_radius(self):
		a, e, _, _, _, _ = vector_to_coes(self.r0, self.v0)
		ra = a*(1+e)
		return ra

class TwoBodyEphemeris:
	def __init__(self, r, v, epoch):
		self.two_body_model = TwoBodyModel(r, v, epoch)
		header_file = pkg_resources.resource_filename(
			__name__, 
			"resources/template_files/ephem_header"
		)
		with open(header_file, "r") as f:
			self.ephem_file_lines = f.readlines()
		self.ephem_file_lines [3] = self.ephem_file_lines [3].replace(
			"stk_date", 
			self.two_body_model.epoch0.to_string_format(STK_EPOCH_FMT)
		)

		self.ephem_count = 0
		self.two_body_models = []
		self.longitudes = []
		self.altitudes = []
		self.burn_longitudes = []
		self.burn_altitudes = []

	@classmethod
	def from_two_body_model(self, two_body_model):
		return self(two_body_model.r0, two_body_model.v0, two_body_model.epoch0)

	def store_point(self, is_maneuver=False):
		self.ephem_file_lines.insert(-1, self.two_body_model.get_ephem_line())
		self.longitudes.append(self.two_body_model.get_longitude())
		self.altitudes.append(self.two_body_model.get_geo_altitude())
		self.two_body_models.append(
			TwoBodyModel(
				self.two_body_model.r0, 
				self.two_body_model.v0, 
				self.two_body_model.epoch0
			)
		)
		if is_maneuver:
			self.burn_longitudes.append(self.longitudes[-1])
			self.burn_altitudes.append(self.altitudes[-1])
		self.ephem_count+=1

	def step_to_epoch(self, epoch):
		self.two_body_model.step_to_epoch(epoch)
		self.store_point()

	def maneuver_at_epoch(self, epoch, ric_burn):
		self.two_body_model.maneuver_at_epoch(epoch, ric_burn)
		self.store_point(True)

	def write_ephem_to_file(self, filename):
		self.ephem_file_lines[2] = self.ephem_file_lines [2].replace(
			"stk_points", 
			"%d" % self.ephem_count
		)
		with open(filename, "w") as f:
			for line in self.ephem_file_lines:
				f.write(line)

	def generate_ephemeris(
		self, 
		duration, 
		step_size, 
		dv_time_list=[], 
		dv_list=[]
	):
		self.ephem_count = 0
		self.two_body_models = []
		self.longitudes = []
		self.altitudes = []
		self.burn_longitudes = []
		self.burn_altitudes = []
		t = 0
		apply_burn = False
		while t < duration:
			apply_burn = False
			if len(dv_time_list) > 0:
				if t >= dv_time_list[0]:
					old_t = t
					t = dv_time_list[0]
					burn = dv_list[0]
					del dv_time_list[0]
					del dv_list[0]
					apply_burn = True

			if apply_burn:
				self.maneuver_at_epoch(
					self.two_body_model.ephem_start_epoch.add_seconds(t),
					burn
				)
				t = old_t
			else:
				self.step_to_epoch(
					self.two_body_model.ephem_start_epoch.add_seconds(t)
				)
			t+=step_size


class ClohessyWiltshireModel:
	"""
	This class performs calculations of relative satellite positions using 
	Clohessy-Wiltshire equations defined in 'Fundamentals of Astrodynamics and 
	Applications' by David Vallado.
	"""
	
	def __init__(self, t0_state, a):
		"""
		Defines starting state for two spacecraft given the state of chase 
		relative to target at time == 0
		
		@type t0_state:  	an enumeration of floats
		@param t0_state: 	[x, y, z, x_dot, y_dot, z_dot] in meters and meters 
							per second respectively.  The values x, y, z 
							represent radial, in-track, and cross-track.
		@type a:			number
		@param a:			Average altitude of target spacecraft                       
		@rtype:         	None
		@return:        	N/A
		"""
		
		#Save input state as a vector
		self.init_state = Vector(t0_state)
		self.position = Vector(t0_state[0:3])
		self.velocity = Vector(t0_state[3:6])

		
		#Save orbital rate internally to prevent future repetitive calculations
		self.a = a
		self.n = sqrt((Earth().mu/a**3))
	
	def get_system_matrix(self, t):
		"""
		Returns the system of CW equations in matrix form.
		
		@type t:			number
		@param t:			Number of seconds from the initial state epoch
		@rtype:				Matrix
		@return:			Matrix representation of CW equations for time t
		"""
		
		n = self.n
		sn = sin(n*t)
		cs = cos(n*t)
		
		#define system matrix of x, y, z, x_dot, y_dot, z_dot equations
		sys_mat = Matrix([
			[4-3*cs, 0, 0, sn/n, 2*(1-cs)/n, 0],
			[6*(sn-n*t), 1, 0, -2*(1-cs)/n, (4*sn-3*n*t)/n, 0],
			[0, 0, cs, 0, 0, sn/n],
			[3*n*sn, 0, 0, cs, 2*sn, 0],
			[-6*n*(1-cs), 0, 0, -2*sn, 4*cs-3, 0],
			[0, 0, -n*sn, 0, 0, cs]
			])
					
		return sys_mat

	def solve_next_state(self, t):
		"""
		Returns the relative state of the system at time t
		
		@type t:			number
		@param t:			Number of seconds from the initial state epoch
		@rtype:				Vector
		@return:			Future x, y, z, x_dot, y_dot, z_dot in meters and 
							meters per second
		"""
		
		#Get matrix of CW equations for time t
		sys_mat = self.get_system_matrix(t)
					
		return sys_mat.multiply(self.init_state)

	def step_to_time(self, t):
		"""
		Sets the initial state vector to the state at time t

		@type t:			number
		@param t:			Number of seconds from the initial state epoch
		@rtype:				None
		@return:			None
		"""
		
		print(self.solve_next_state(t))
		self = ClohessyWiltshireModel(self.solve_next_state(t), self.a)
		print(self.init_state)
	
	def apply_velocity_change(self, velocity_array):
		"""
		Updates the current relative state by applying a velocity change

		@type velocity_array:	numpy array
		@param velocity_array:	[x, y, z] velocities to add in m/s 
		@rtype:					None
		@return:				N/A
		"""
		
		#Pad the input array with zeros to represent a 6-D state change vector
		state_change_vector = Vector(
			np.pad(velocity_array, [(3, 0), (0, 0)], mode='constant')
			)
		
		#Update current relative state with velocity change incorporated
		self.init_state = self.init_state.plus(state_change_vector)
		self.position = Vector(
			[
				self.init_state.get_element(0),
				self.init_state.get_element(1),
				self.init_state.get_element(2)
			]
		)
		self.velocity = Vector(
			[
				self.init_state.get_element(3),
				self.init_state.get_element(4),
				self.init_state.get_element(5)
			]
		)

		
	def get_positions_over_interval(self, t_i, t_f, dt, scale=1):
		"""
		Returns x, y, and z positions at given timestep over desired interval

		@type t_i:				int
		@param t_i:				Starting time offset of propagation interval
		@type t_f:				int
		@param t_f:				Ending time offset of propagation interval
		@type dt:				int
		@param dt:				step size when propagating
		@rtype:					tuple of lists
		@return:				x, y, and z positions in respective lists
		"""
		
		#Initialize empty lists to hold x, y, and z values of positions
		x, y, z = [], [], []
		
		#Loop through timeframe and append position components to lists
		for t in range(t_i, t_f, dt):
			state = self.solve_next_state(t)
			x.append(state[0][0]/scale)
			y.append(state[1][0]/scale)
			z.append(state[2][0]/scale)
			
		return x, y, z

	def get_clos_over_interval(self, t_i, t_f, dt, expected_geo, expected_gnd):

		#Initialize empty lists to hold x, y, and z values of positions
		times, clos_geo, clos_gnd = [], [], []
		
		#Loop through timeframe and append position components to lists
		for t in range(t_i, t_f, dt):
			state = self.solve_next_state(t)
			tgt_pos = Vector(state[0:3])
			act_geo = expected_geo.plus(tgt_pos)
			act_gnd = expected_gnd.plus(tgt_pos)
			
			geo_ang = expected_geo.angle(act_geo)
			gnd_ang = expected_gnd.angle(act_gnd)
			clos_geo.append(expected_geo.magnitude()*tan(geo_ang)/1000)
			clos_gnd.append(expected_gnd.magnitude()*tan(gnd_ang)/1000)
			times.append(t/3600)

			
		return times, clos_geo, clos_gnd

	def get_close_approach_over_interval(self, t_i, t_f, dt):
		
		min_range = None
		ca_time = None

		#Loop through timeframe and append position components to lists
		for t in range(t_i, t_f, dt):
			state = self.solve_next_state(t)
			dist = Vector(state[0:3]).magnitude()
			if min_range is None or dist < min_range:
				min_range = dist
				ca_time = t
			
		return ca_time, min_range

	def get_max_range_over_interval(self, t_i, t_f, dt, scale=1):
		max_range = 0
		ca_time = None

		#Loop through timeframe and append position components to lists
		for t in range(t_i, t_f, dt):
			state = self.solve_next_state(t)
			dist = Vector(state[0:3]).scale(scale).magnitude()
			if dist > max_range:
				max_range = dist
				ca_time = t
			
		return ca_time, max_range

	def get_period(self):
		"""
		Return the number of seconds required to complete a full period

		@rtype:		number
		@return:	number of seconds for full revolution of model
		"""

		return 2*pi/self.n

	def step_to_next_tangent(self):
		"""
		Step the model forward to the next radial tangent

		@rtype:					number
		@return:				number of seconds the model was propagated
		"""
		
		#Save key components from current initial state
		x = self.init_state.get_element(0)
		x_dot = self.init_state.get_element(3)
		y_dot = self.init_state.get_element(4)
		
		#Solve for the time of nearest x_dot==0 occurence
		t = atan(-x_dot/(3*self.n*x + 2*y_dot))/self.n
		
		#Correct t by half period for any negative or 0 solutions
		if t <= ZERO: 
			t += self.get_period()/2
		elif isnan(t):
			t = self.get_period()/2
		
		#Update t0_state to reflect new tangential position
		self.init_state = self.solve_next_state(t)
		self.position = Vector([
			self.init_state.get_element(0),
			self.init_state.get_element(1),
			self.init_state.get_element(2)
		])
		self.velocity = Vector([
			self.init_state.get_element(3),
			self.init_state.get_element(4),
			self.init_state.get_element(5)
		])
		
		return t
		
		
	def solve_four_burns_to_match_xy(self, wp_seconds_from_now):
		"""
		Solve the four-burn sequence that creates a circular phasing altitude 
		(two burns) relative to the desired orbit state, ingresses to a 0 
		waypoint (1 burn) then matches velocity at the input waypoint time 
		(1 burn).  This method should only be used when starting at an altitude
		tangent.  Otherwise, the assumptions used to simplify the algebra will 
		be invalid.

		@type wp_seconds_from_now:		number
		@param wp_seconds_from_now:		The time of the last velocity-targeting
										burn in seconds from now
		@rtype:							tuple
		@return:						The in-track burn magnitudes of each 
										burn in the order (phasing burn 1, 
										recirc burn, ingress burn, velocity 
										match burn)
		"""

		#Store key constants to reduce clutter in system matrix
		n = self.n
		t_hp = self.get_period()/2
		t_Tp = wp_seconds_from_now - self.get_period()
		xi = self.init_state[0][0]
		yi = self.init_state[1][0]
		sn = sin(n*t_Tp)

		#Save system matrix and solution vectors.  
		soln_vector = Vector([7*xi, 0, 0, -6*xi*n*t_hp + yi, 0, 0, 0])
		sys_mat = Matrix([
					[0, 0, 0, 1, -4/n, 0, 0],
					[0, 0, 0, -6, 0, -4/n, 0],
					[0, 0, 0, 1, 0, 0, -4/n],
					[1, 0, 0, 0, 3*t_hp, 0, 0],
					[-1, 1, 0, -6*(sn-n*t_Tp), 0, -(4*sn - 3*n*t_Tp)/n, 0],
					[0, 0, 1, 0, 0, 0, -3*t_hp],
					[0, 1, -1, 0, 0, 0, 0]
		])
		
		#Find the results for [y1, y2, y3, x_phasing, y_dot1, y_dot2, y_dot3]
		result = sys_mat.get_inverse().multiply(soln_vector)

		#Burn #1 is the difference of the desired y_dot1 and the current y_dot
		burn1 = Vector(
			[0, result.get_element(4)-self.init_state.get_element(4), 0]
			)

		#Copy the current model to perform burns and solve the remaining burns
		phase_model = ClohessyWiltshireModel(self.init_state, self.a)

		#Maneuver the model into the pre-circular phasing orbit
		phase_model.apply_velocity_change(burn1)

		#Step to the next tangent to recircularize at the desired altitude
		phase_model.step_to_next_tangent()

		#Burn #2 is the difference of the desired y_dot2 and the phasing y_dot
		burn2 = Vector(
			[0, result.get_element(5)-phase_model.init_state.get_element(4), 0]
			)

		#Maneuver the model to achieve a circular phasing orbit
		phase_model.apply_velocity_change(burn2)

		#Create an ingress model formed at a 0 waypoint
		ingress_model = ClohessyWiltshireModel(
			[0, 0, 0, 0, result.get_element(6), 0], 
			self.a
			)

		#Step backwards half a period to the ingress point
		state = ingress_model.solve_next_state(-ingress_model.get_period()/2)

		#Achieve the same position as the ingress model
		state2 = phase_model.solve_next_state(t_Tp - t_hp)

		#Burn #3 is the difference of the ingress y_dot and the phasing y_dot
		burn3 = Vector([0, state.get_element(4) - state2.get_element(4), 0])

		#Burn #4 is the anti-vector of the solved y_dot3 value
		burn4 = Vector([0, -result.get_element(6), 0])

		return burn1, burn2, burn3, burn4, t_Tp
		
	def solve_three_burns_to_match_xy(self, wp_seconds_from_now):
		"""
		Solve the three-burn sequence that phases (1 burn), ingresses (1 burn),
		then matches velocity BEFORE the input waypoint time (1 burn).  This 
		method should only be used when starting at an altitude tangent.  
		Otherwise, the assumptions used to simplify the algebra will be invalid.
		The final burn time will be chose based on the number of full periods 
		between now and the input waypoint time

		@type wp_seconds_from_now:		number
		@param wp_seconds_from_now:		The latest time of the last velocity-
										targeting burn in seconds from now
		@rtype:							tuple
		@return:						The in-track burn magnitudes of each 
										burn in the order (phasing burn 1, 
										recirc burn, ingress burn, velocity 
										match burn)
		"""

		#Store key constants to reduce clutter in system matrix
		n = self.n
		t_hp = self.get_period()/2
		total_periods = wp_seconds_from_now % self.get_period()
		t_Tp = (wp_seconds_from_now - total_periods) - t_hp
		xi = self.init_state.get_element(0)
		yi = self.init_state.get_element(1)

		#Save system matrix and solution vectors.  
		soln_vector = Vector(
			[7*xi, 0, -6*xi*n*t_hp + yi, 0, -6*xi*n*t_Tp + yi, 0]
			)

		sys_mat = Matrix([
					[0, 0, 0, 1, -4/n, 0],
					[0, 0, 0, 1, 0, -4/n], 
					[1, 0, 0, 0, 3*t_hp, 0],
					[0, 1, 0, 0, 0, -3*t_hp],
					[0, 0, 1, 0, 3*t_Tp, 0],
					[0, -1, 1, 0, 0, 0]
		])
		
		#Find the results for [y1, y2, y3, x_phasing, y_dot1, y_dot2, y_dot3]
		result = sys_mat.get_inverse().multiply(soln_vector)

		#Burn #1 is the difference of the desired y_dot1 and the current y_dot 
		burn1 = Vector(
			[0, result.get_element(4) - self.init_state.get_element(4), 0]
			)

		#Copy the current model to perform burns and solve the remaining burns
		phase_model = ClohessyWiltshireModel(self.init_state, self.a)

		#Maneuver the model into the phasing orbit
		phase_model.apply_velocity_change(burn1)

		#Create an ingress model formed at a 0 waypoint
		ingress_model = ClohessyWiltshireModel(
			[0, 0, 0, 0, result.get_element(5), 0], 
			self.a
			)

		#Step backwards half a period to the ingress point
		state = ingress_model.solve_next_state(-ingress_model.get_period()/2)

		#Achieve the same position as the ingress model
		state2 = phase_model.solve_next_state(t_Tp)

		#Burn #2 is the difference of the ingress y_dot and the phasing y_dot
		burn2 = Vector([0, state.get_element(4) - state2.get_element(4), 0])

		#Burn #3 is the anti-vector of the solved y_dot3 value
		burn3 = Vector([0, -result.get_element(5), 0])

		return burn1, burn2, burn3, t_Tp

	def solve_waypoint_burn(self, t, wp, solve_c=True):
		"""
		Returns velocity change required to hit a waypoint in a time (t)
		
		@type t:			number
		@param t:			Number of seconds from the initial state epoch
		@type wp:			numpy array
		@param wp:			Desired positional offset to achieve
		@rtype:				numpy array
		@return:			Velocity difference required to achieve waypoint
		"""
		
		#Get matrix of CW equations for time t
		sys_mat = self.get_system_matrix(t)
		
		#Solve constant side of linear system using first 3 equations in CW 
		#matrix.  This is possible because starting and stopping positions are 
		#known over given interval.  We are left with 3 unknown velocities and 
		#3 equations 
		pos = Vector(self.init_state[0:3])
		vel = Vector(self.init_state[3:6])
		pos_equation_mat = Matrix(sys_mat[0:3, 0:3])
		soln_vector = wp.minus(pos_equation_mat.multiply(pos))
		
		#Isolate velocity portions of previously mentioned CW equations
		velocity_mat = Matrix(sys_mat[0:3, 3:6])
		
		#Save difference of desired velocity and current velocity to represent required burn magnitude
		result = velocity_mat.get_inverse().multiply(soln_vector).minus(vel)
		
		if not solve_c:
			result[2][0] = 0
			
		return result
