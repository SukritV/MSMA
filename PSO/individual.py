import numpy as np
from particle import calc_w

class Individual:
	def __init__(self, config, name = "noname"):
		"Builds an Individual object"
		self.name = name # name to identify the particle
		self.fitness = 0 # a double, current fitness score
		
		# using config data
		self.num_discrete = config.num_discrete
		self.num_continuous = config.num_continuous
		self.num_interactions = config.num_interactions
		self.b = np.asarray(config.b) # input beta values
		self.ub = np.asarray(config.ub)
		self.lb = np.asarray(config.lb)
		self.link = config.link_fn_name
		self.interactions = config.interactions

		self.nrows = 2 ** (self.num_discrete + self.num_continuous)
		self.ncols = 1 + self.num_discrete + \
			self.num_continuous + self.num_interactions

		self.design = self._gen_design_matrix() # a design matrix
		self.fisher_info = None # information matrix
		self.p = np.random.random(self.nrows) # a vector of proportions/probabilities
		self._normalize_p()

	def __repr__(self):
		return repr(self.get_included_design())
		
	def _normalize_p(self):
		"sum of p_i's should equal 1 for it to be a probability distribution"
		self.p = self.p / sum(self.p)

	def _gen_boundary_frame(self):
		dim = self.num_discrete + self.num_continuous
		boundframe = np.zeros((self.nrows, dim))
		for col in range(dim):
			flipcount = 2 ** (dim - col -1)
			lowerbound, counter = True, 0
			for row in range(self.nrows):
				boundframe[row][col] = self.lb[col] if lowerbound else self.ub[col]
				counter += 1
				if counter == flipcount:
					counter = 0
					lowerbound = not lowerbound
		return boundframe, dim

	def _gen_design_matrix(self):
		design = np.zeros((self.nrows, self.ncols))
		boundframe, dim = self._gen_boundary_frame()
		for i in xrange(self.nrows):
			design[i][0] = 1
			if self.num_discrete > 0:
				for col in range(1,1+self.num_discrete):
					design[i][col] = boundframe[i][col-1]
				for col in range(1+self.num_discrete,1+dim):
					design[i][col] = np.random.random()
			if self.num_discrete < 1:
				for col in range(1,1+dim):
					design[i][col] = np.random.random()

		# Now we want to add in the interaction columns
		# plan: loop through interactions and then multiple by indices
		intstart = 1 + self.num_discrete + self.num_continuous;
		for row in xrange(self.nrows):
			for i, interaction in enumerate(self.interactions):
				design[row][intstart+i] = 1
				for index in interaction:
					design[row][intstart+i] *= design[row][index]
		return design

	def get_included_design(self):
		"this is of type Design Object's finaldesign in design module"
		filtered_rows = []
		filtered_p = []
		ncols = 1 + self.num_discrete + self.num_continuous
		for i, row in enumerate(self.design):
			if self.p[i] > 0.04: # neglect low proportion rows
				filtered_rows.append(row[:ncols+1])
				filtered_p.append(self.p[i])

		return {"design_matrix": filtered_rows, 
			"proportions": filtered_p}

	def print_included_design(self):
		print "Included Design in individual %s" % self.name
		included_design = self.get_included_design()
		for row, prop in zip(included_design["design_matrix"], 
			included_design["proportions"]):
			print " ".join(map(lambda x: "%.2f" % x, row)) + " | " + str(prop)
		
	def calc_fisher(self):
		W = np.asarray(np.zeros((self.nrows,1)))
		for i in xrange(self.nrows):
			xb = np.dot(self.b, self.design[i])
			W[i] = calc_w(xb, self.link) * self.p[i]
		# fisher_info <- X'WX where W is diagonal matrix
		XtW = self.design.T * np.dot(np.ones((self.ncols,1)),W.T)
		self.fisher_info = np.dot(XtW, self.design) # (X' * W) * X part

	def calc_fitness(self):
		self.calc_fisher()
		self.fitness = np.linalg.det(self.fisher_info)

if __name__ == '__main__':
	# test driver code
	from config import Config 
	config = Config(num_discrete=2, num_continuous=3, num_interactions=2, 
		interactions=[(1,2),(3,3)], b=np.random.random(8).tolist(), 
		lb=[-1,-2,-1,-2,-3], ub=[1,2,1,2,3],
		max_iter=10, num_particles=25, link_fn_name="logit")
	print config

	# test methods of Particle class
	individual = Individual(config, name="Individual001")
	individual.print_included_design()
	individual.calc_fisher()
	individual.calc_fitness()

