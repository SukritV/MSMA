class Config:
	"Has all the configuration data needed to run the algorithm"
	def __init__(self, num_discrete = None, num_continuous = None, b = None,
		num_interactions = None, interactions = None, lb = None, ub = None,
		max_iter = None, num_particles = None, link_fn_name = None,
		max_resets = None, leb = None, max_iter2 = None, mutation_prob = None,
		survival_rate = None, elitism_rate = None, stage2_selection_rate = None,
		mutation_prob2 = None, survival_rate2 = None, elitism_rate2 = None):

		self.num_discrete = num_discrete # an int, number of discrete factors
		self.num_continuous = num_continuous # an int, number of continuous factors
		self.num_interactions = num_interactions # an int, number of interaction terms
		
		self.b = b # a list of beta values
		assert(len(self.b) == \
			1 + self.num_discrete + self.num_continuous + self.num_interactions)

		self.interactions = interactions # a list of pairs of int, representing the 
		# interaction. Eg: [(1,2),(3,3)] is the interaction term for x_1 x_2 and x_3^2
		assert(len(self.interactions) == self.num_interactions) # make sure that the 
		# length matches

		self.lb = lb # a list of doubles for lower bounds of each factor
		self.ub = ub # a list of doubles for upper bounds of each factor, firstly for
		# the discrete factors and next for the continuous factors

		assert(len(self.lb) == len(self.ub) == self.num_discrete + self.num_continuous)

		self.max_iter = max_iter # maximum number of iterations to perform
		self.num_particles = num_particles # number of particles to use in PSO
		self.link_fn_name = link_fn_name # a string, for link function

		# make sure that the link function name is valid one
		assert(self.link_fn_name in ["logit","probit","loglog","cloglog"])
		self.max_resets = max_resets
		self.leb = leb

		# below config parameter used by MSMA only
		self.max_iter2 = max_iter2
		self.mutation_prob = mutation_prob
		self.survival_rate = survival_rate
		self.elitism_rate = elitism_rate
		self.stage2_selection_rate = stage2_selection_rate
		self.mutation_prob2 = mutation_prob2
		self.survival_rate2 = survival_rate2
		self.elitism_rate2 = elitism_rate2

	def __repr__(self):
		betas_str = "[" + ", ".join(map(lambda x: "%.2f" % x, self.b)) + "]"
		return ("<Config: \n  num_discrete=%s\n  num_continuous=%s\n  num_interactions=%s\n" \
			 + "  interactions=%s\n  lb=%s\n  ub=%s\n  b=%s\n  max_iter=%s\n" \
			 + "num_particles=%s\n  link_fn_name=%s\n  max_resets=%s\n  leb=%s >\n") % \
				((str(self.num_discrete), str(self.num_continuous),
				self.num_interactions, str(self.interactions), str(self.lb),
				str(self.ub), betas_str, str(self.max_iter), str(self.num_particles),
				str(self.link_fn_name), str(self.max_resets), str(self.leb)))

# Format for config
# (int num_parts, std::vector<double> lbd, std::vector<double> ubd, 
# 	int maxit, int num_discrete, int num_continuous, int num_interactions, 
# 	std::vector<std::vector <int> > interact, std::vector<double >b, 
# 	int maxresets, double lower_efficiency_bound, std::string link)

configs = [
	# index 0
	# make sure interactions are counted; this is long term example
	Config(num_particles=5,
		lb=[-1, -1, -1, -1],
		ub=[1, 1, 1, 1],
		max_iter=200,
		num_discrete=4,
		num_continuous=0,
		num_interactions=2,
		interactions=[(1,2), (1,3)],
		b=[0.1, 0.2, 0.3, 0.45, 0.25, 0.8, 0.4],
		max_resets=100,
		leb=0.999,
		link_fn_name="logit"),
	# index 1
	# Dror and Steinberg 2006 Example
	Config(num_particles=50,
		lb=[-1, -1],
		ub=[1, 1],
		max_iter=100,
		num_discrete=1,
		num_continuous=1,
		num_interactions=1,
		interactions=[(1,2)],
		b=[1, 2, 2, 0.2],
		max_resets=1000,
		leb=0.999,
		link_fn_name="logit"),
	# index 2
	#na example
	Config(num_particles=50,
		lb=[-1, -1],
		ub=[1, 1],
		max_iter=150,
		num_discrete=1,
		num_continuous=1,
		num_interactions=0,
		interactions=[],
		b=[1, -2.9, -0.3],
		max_resets=200,
		leb=0.99,
		link_fn_name="cloglog"),
	# index 3
	Config(num_particles=50,
		lb=[-1, -1],
		ub=[1, 1],
		max_iter=150,
		num_discrete=1,
		num_continuous=1,
		num_interactions=1,
		interactions=[(1,2)],
		b=[1, -3, -0.8, 0.25],
		max_resets=50,
		leb=0.99,
		link_fn_name="logit"),
	# index 4
	Config(num_particles=50,
		lb=[-1, -1],
		ub=[1, 1],
		max_iter=150,
		num_discrete=1,
		num_continuous=1,
		num_interactions=0,
		interactions=[],
		b=[0.5, 0.4, 0.3],
		max_resets=100,
		leb=0.99,
		link_fn_name="loglog"),
	# index 5
	Config(num_particles=50,
		lb=[-1, -1],
		ub=[1, 1],
		max_iter=150,
		num_discrete=1,
		num_continuous=1,
		num_interactions=0,
		interactions=[],
		b=[1, 1, 1],
		max_resets=100,
		leb=0.99,
		link_fn_name="probit"),
	# Voltage example
	# index 6
	Config(num_particles=50,
		lb=[-1, -1, -1, -1, 25],
		ub=[1, 1, 1, 1, 45],
		max_iter=100,
		num_discrete=4,
		num_continuous=1,
		num_interactions=0,
		interactions=[],
		b=[-7.5, 1.5, -0.2, -0.15, 0.25, 0.35],
		max_resets=100,
		leb=0.99,
		link_fn_name="logit"),
	# with interaction
	# index 7
	Config(num_particles=25,
		lb=[-1, -1, -1, -1, 25],
		ub=[1, 1, 1, 1, 45],
		max_iter=10,
		num_discrete=4,
		num_continuous=1,
		num_interactions=1,
		interactions=[(3,4)],
		b=[-7.5, 1.5, -0.2, -0.15, 0.25, 0.35, 0.4],
		max_resets=50,
		leb=0.99,
		link_fn_name="probit"),
	# index 8
	Config(num_particles=75,
		lb=[-1, -1, -1, -1, 25],
		ub=[1, 1, 1, 1, 45],
		max_iter=100,
		num_discrete=4,
		num_continuous=1,
		num_interactions=1,
		interactions=[(3,4)],
		b=[-7.5, 1.5, -0.2, -0.15, 0.25, 0.35, 0.4],
		max_resets=100,
		leb=0.99,
		link_fn_name="cloglog"),
	# index 9
	# TURN CONVERGE AND LEB BACK ON in two places
	Config(num_particles=25,
		lb=[-1, -1, -1, -1, 50, 30, 0, 18, 0.125, 5],
		ub=[1, 1, 1, 1, 90, 55, 10, 48, 0.425, 15],
		max_iter=40,
		num_discrete=4,
		num_continuous=6,
		num_interactions=0,
		interactions=[],
		b=[-1, 0.2, 0.1, 0.14, 0.06, -0.01, -0.02, -0.02, -0.03, 0.1, 0.03],
		max_resets=20,
		leb=0.99,
		link_fn_name="logit"),
	# index 10
	# unbounded temp and pressure example
	Config(num_particles=150,
		lb=[450, 1100],
		ub=[460, 1300],
		max_iter=260,
		num_discrete=0,
		num_continuous=2,
		num_interactions=0,
		interactions=[],
		b=[0.05, 0.003, 0.007],
		max_resets=100,
		leb=0.999,
		link_fn_name="logit"),
	# index 11
	Config(num_particles=40,
		lb=[-1, -1],
		ub=[1, 1],
		max_iter=100,
		num_discrete=1,
		num_continuous=1,
		num_interactions=0,
		interactions=[],
		b=[0.5, 0.7, 0.3],
		max_resets=100,
		leb=0.995,
		link_fn_name="logit"),
	# index 12
	Config(num_particles=250,
		lb=[-1, -1, -1, -1, 20],
		ub=[1, 1, 1, 1, 30],
		max_iter=100,
		num_discrete=4,
		num_continuous=1,
		num_interactions=0,
		interactions=[],
		b=[0.5, 0.7, 0.3, -0.5, -0.05, -0.15],
		max_resets=100,
		leb=0.995,
		link_fn_name="logit"),
	# index 13
	# 4 discrete and 4 continuous; no interaction
	Config(num_particles=100,
		   lb=[-1, -1, -1, -1, -1,-1,-1,-1],
		   ub=[1, 1, 1, 1, 1, 1, 1, 1],
		   max_iter=250,
		   num_discrete=4,
		   num_continuous=4,
		   num_interactions=0,
		   interactions=[],
		   b=[0.5, 0.7, 0.3, -0.5, -0.05, -0.15, 1, -0.57, -0.2],
		   max_resets=100,
		   leb=0.995,
		   link_fn_name="logit"),
	# index 14
	# make sure interactions are counted; this is long term example
	Config(num_particles=15,
		   lb=[-1, -1],
		   ub=[1, 1],
		   max_iter=200,
		   num_discrete=1,
		   num_continuous=1,
		   num_interactions=0,
		   interactions=[],
		   b=[0.1, 0.2, 0.3],
		   max_resets=40,
		   leb=0.999,
		   link_fn_name="logit"),
	]

if __name__ == '__main__':
	print configs
