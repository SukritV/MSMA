import numpy as np
import random, math


def calc_w(xb, link):
	"""
		Function to calculate the W value based on the 
		linear predictor and the link function
	"""
	w = 0
	if link == "logit":
		w = (math.exp(xb) / ( (1 + math.exp(xb)) * (1 + math.exp(xb)) ) )
	elif link == "cloglog":
		w = (math.exp(math.exp(xb)) - 1) * pow(log(1 - math.exp(-math.exp(xb))), 2)
	elif link == "loglog":
		w = (math.exp((2*xb) - math.exp(xb))) / (1 - math.exp(-math.exp(xb)))
	elif link == "probit":
		num = (math.exp(-.5*(xb*xb)) / math.sqrt(2*math.pi));
		current = xb;
		iteration_sum = xb;
		for i in range(1,50):
			iteration_sum = (iteration_sum * xb * xb / (2*i+1));
			current = current + iteration_sum;
		
		cdf = 0.5 + (current / math.sqrt(2*math.pi)) * math.exp(-(xb*xb)/2);
		w = (num*num) / (cdf * (1 - cdf));
		if w > 1:
			w = 0
	else:
		# this will never execute
		print "[WARN] invalid link function \"%s\" specified" % link
		exit() 
	return w

class Particle:
	"Represents a unit in the swarm of PSO"
	def __init__(self, config, name = "noname"):
		"Builds a Particle object"
		self.name = name # name to identify the particle
		self.pbest = 0 # a double, personal best fitness score
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
		self.v0 = np.zeros((self.nrows,self.ncols - self.num_interactions)) 
			# a matrix for the velocity
		self.pbest_pos = np.copy(self.design) # position of the pbest
		self.fisher_info = None # information matrix
		self.decomp = None
		self.p = np.random.random(self.nrows) # a vector of proportions/probabilities
		self._normalize_p()
		self.pbest_p = np.copy(self.p)
		self.vp = np.zeros(self.nrows) # a velocity vector for p

	def _normalize_p(self):
		"sum of p_i's should equal 1 for it to be a probability distribution"
		self.p = abs(self.p) / sum(abs(self.p))

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
		for i, row in enumerate(self.pbest_pos):
			if self.pbest_p[i] > 0.04: # neglect low proportion rows
				filtered_rows.append(row[:ncols+1])
				filtered_p.append(self.pbest_p[i])

		return {"design_matrix": filtered_rows, 
			"proportions": filtered_p}

	def print_included_design(self):
		print "Included Design in particle %s" % self.name
		included_design = self.get_included_design()
		for row, prop in zip(included_design["design_matrix"], 
			included_design["proportions"]):
			print " ".join(map(lambda x: "%.2f" % x, row)) + " | " + str(prop)
	
	def set_pbest_pos(self):
		self.pbest_pos = np.copy(self.design)
		self.pbest_p = np.copy(self.p)
	
	def calc_fisher(self):
		W = np.asarray(np.zeros((self.nrows,1)))
		for i in xrange(self.nrows):
			xb = np.dot(self.b, self.design[i])
			W[i] = calc_w(xb, self.link) * self.p[i]
		# fisher_info <- X'WX where W is diagonal matrix
		XtW = self.design.T * np.dot(np.ones((self.ncols,1)),W.T)
		self.fisher_info = np.dot(XtW, self.design) # (X' * W) * X part

	def calc_fitness(self):
		self.fitness = np.linalg.det(self.fisher_info)
		if self.fitness > self.pbest:
			self.pbest = self.fitness
			self.set_pbest_pos()

	def update_velocity(self, gbest_position, gbest_p, inertia):
		# loop over each design point and update the velocity
		for i in xrange(self.nrows):
			for j in range(1+self.num_discrete,self.ncols - self.num_interactions):
				v_prev = inertia * self.v0[i][j]
				cognitive = 2 * np.random.random() * (self.pbest_pos[i][j] - self.design[i][j])
				social = 2 * np.random.random() * (gbest_position[i][j] - self.design[i][j])
				self.v0[i][j] = v_prev + cognitive + social
				if abs(self.v0[i][j]) > self.ub[j-1]:
					self.v0[i][j] = (self.v0[i][j] / abs(self.v0[i][j])) * self.ub[j-1];

			pv_prev = inertia * self.vp[i];
			pcognitive = 2 * np.random.random() * (self.pbest_p[i] - self.p[i]);
			psocial = 2 * np.random.random() * (gbest_p[i] - self.p[i]);
			self.vp[i] = pv_prev + pcognitive + psocial;
			if abs(self.vp[i]) > 1:
				self.vp[i] = self.vp[i] / abs(self.vp[i]);
        
	def update_position(self):
		for i in xrange(self.nrows):
			for j in range(1+self.num_discrete,self.ncols - self.num_interactions):
				self.design[i][j] = self.design[i][j] + self.v0[i][j]
			self.p[i] = self.p[i] + self.vp[i]
		# now need to update the interactions
		intstart = 1 + self.num_discrete + self.num_continuous;
		for row in xrange(self.nrows):
			for i, interaction in enumerate(self.interactions):
				self.design[row][intstart+i] = 1
				for index in interaction:
					self.design[row][intstart+i] *= self.design[row][index]

	def fix_bounds(self):
		for i in xrange(self.nrows):
			for j in range(1+self.num_discrete,self.ncols - self.num_interactions):
			# handle too large
				if self.design[i][j] > self.ub[j-1]:
					oldpos = self.design[i][j]
					self.design[i][j] = self.ub[j-1]
					difference = oldpos - self.design[i][j]
					self.v0[i][j] = self.v0[i][j] - difference

				#handle too small
				if self.design[i][j] < self.lb[j-1]:
					oldpos = self.design[i][j]
					self.design[i][j] = self.lb[j-1]
					difference = oldpos - self.design[i][j]
					self.v0[i][j] = self.v0[i][j] - difference
		
		p_total = sum(map(abs, self.p))
		for i in xrange(self.nrows):
			oldpos = self.p[i]
			self.p[i] = abs(self.p[i]) / p_total
			self.vp[i] = self.vp[i] - (oldpos - self.p[i])

		# now need to update the interactions
		intstart = 1 + self.num_discrete + self.num_continuous;
		for row in xrange(self.nrows):
			for i, interaction in enumerate(self.interactions):
				self.design[row][intstart+i] = 1
				for index in interaction:
					self.design[row][intstart+i] *= self.design[row][index]

	def check_dups(self):

		dim = 1 + self.num_continuous + self.num_discrete
		cara_num = pow(2, (dim-1))

		for comprow in xrange(cara_num):
			for row in range(comprow+1, cara_num):
				rowcomp = 0	
				for col in range(1,dim):
					rowcomp += abs(self.pbest_pos[comprow][col] - self.pbest_pos[row][col])

				if rowcomp < 0.05:
					# we need to figure out which had alarger prop allocated to it
					diff = self.pbest_p[comprow] - self.pbest_p[row]
					replace_index = row #default to replacing the lower row
					add_index = rowcomp
					if diff < 0:
						replace_index = comprow
						add_index = row
				
					# add one row to the other
					self.pbest_p[add_index] += self.pbest_p[replace_index]
					self.pbest_p[replace_index] = 0

if __name__ == '__main__':
	# test driver code
	from config import Config 
	config = Config(num_discrete=2, num_continuous=3, num_interactions=2, 
		interactions=[(1,2),(3,3)], b=np.random.random(8).tolist(), 
		lb=[-1,-2,-1,-2,-3], ub=[1,2,1,2,3],
		max_iter=10, num_particles=25, link_fn_name="logit")
	print config

	# test methods of Particle class
	particle = Particle(config, name="Particle001")
	particle.print_included_design()
	particle.calc_fisher()
	particle.calc_fitness()
	particle.update_velocity(particle.pbest_pos, particle.pbest_p, 0.9)
	particle.update_position()
	particle.fix_bounds()
	particle.check_dups()