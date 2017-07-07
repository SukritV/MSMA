class Design:
	"Encapsulates a Design"
	def __init__(self):
		"Constructor, initializes a Design object"
		self.gbest = 0 # a double, which is the fitness score of the global best
		self.leb = 0 # lower efficiency bound
		self.converged = False # a bool, to indicate convergence
		self.size = 0
		# design_matrix is the combinations for experimental settings
		# proportion is vector of probability, which gives weightage to the rows
		# in design_matrix
		self.finaldesign = { "design_matrix": None , "proportion": None}

	def __repr__(self):
		"Tells how to print/represent itself (a Design object)"
		return "<Design: gbest=%s leb=%s converged=%s size=%s>" % \
			((str(self.gbest),str(self.leb),str(self.converged),
				str(self.size))) #\
			#+ "\nfinal_design: \n" + repr(self.finaldesign)

if __name__ == '__main__':
	#test case 0
	design = Design()
	print design