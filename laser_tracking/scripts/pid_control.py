class PID(object):
	"""PID controller where
	Command = P*p_error + I*i_error + d*d_error
	"""
	def __init__(self,P,I,D):
		P = 1;
		I = 1;
		D = 0;
		Perror = 0;
		Ierror = 0;
		Derror = 0;
		Perror_last = 0;
		cmd = 0

	def set_gains(self,P_gain,I_gain,D_gain):
		self.P = P_gain
		self.I = I_gain
		self.D = D_gain

	def update(self,p_error,dt):
		"""Update the PID loop, return the command velocity
		p_error = Error since the last update: state-target
		dt = change in time since last call
		"""
		Perror = p_error

		if dt == 0:
			return 0.0

		#Proportional Term:
		p_term = self.P * p_error

		#Integral term
		self.Ierror += self.Perror * dt
		i_term = self.I * self.Ierror

		#Derivative term
		self.Derror = (self.Perror - self.Perror_last) / dt
		self.Perror_last = self.Perror
		d_term = self.D * self.Derror

		#Calculate and return the command velocity:
		self.cmd = -p_term - i_term - d_term
		return self.cmd

