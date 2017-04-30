class PID(object):
	"""PID controller where
	Command = P*p_error + I*i_error + d*d_error
	"""
	def __init__(self,P_gain,I_gain,D_gain,I_max):
		self.P = P_gain
		self.I = I_gain
		self.D = D_gain
		self.I_max = I_max
		self.Perror = 0.0
		self.Ierror = 0.0
		self.Derror = 0.0
		self.Perror_last = 0.0
		self.p_term = 0.0
		self.i_term =0.0
		self.d_term =0.0
		self.cmd = 0.0
		self.t_last = 0.0

	def set_gains(self,P_gain,I_gain,D_gain):
		self.P = P_gain
		self.I = I_gain
		self.D = D_gain

	def update(self,p_error,t_now):
		"""Update the PID loop, return the command velocity
		p_error = Error since the last update: state-target
		dt = change in time since last call
		"""
		self.Perror = p_error

		if self.t_last == 0:
			self.t_last = t_now
			return 0.0
		else:
			dt = t_now-self.t_last
		self.t_last = t_now
		#Proportional Term:
		self.p_term = self.P * self.Perror

		#Integral term
		self.Ierror += self.Perror * dt
		self.Ierror = max(min(self.Ierror,self.I_max),-self.I_max) #limit |i_term| under i_max
		self.i_term = self.I * self.Ierror
		

		#Derivative term
		self.Derror = (self.Perror - self.Perror_last) / dt
		self.Perror_last = self.Perror
		self.d_term = self.D * self.Derror

		#Calculate and return the command velocity:
		self.cmd = -self.p_term - self.i_term - self.d_term
		return self.cmd

	def debug(self):
		return "Pterm:%f Iterm:%f, Dterm:%f,Sum=%f"%(self.p_term, self.i_term, self.d_term, self.cmd)