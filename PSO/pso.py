from particle import Particle, calc_w
import numpy as np, math
from design import Design

def calc_gbest(swarm):
	"function to calculate the global best fitness value"
	gbest = max(map(lambda x: x.pbest, swarm))

def pointPicker(num_continuous, current, checker, checkSize):
	if current[checker] < checkSize:
		current[checker] = current[checker] + 1; # need to change 1 to incrementor
		return current 
	# handle when a variable is maxed out
	else:
		for resetter in range(checker,num_continuous): 
			current[resetter] = 0

		# need to add check if checker == 0
		if checker > 0:
			current = pointPicker(num_continuous, current, checker-1, checkSize); 
	# final return statement (otherwise can get stuck)
	return current

# below functions need porting
def equivalance_check(fisher_information, gbest_position, gbest_p, lb, ub,
	num_discrete, num_continuous, num_interactions, interactions, b,
	lower_equivalence_bound, link):
	
	dim = num_continuous + num_discrete + 1 + num_interactions
	nrow = pow(2, num_discrete+num_continuous)
	threshold = -dim * np.log(lower_equivalence_bound)
	pass_check = True

	# first we need to find the inverse of the information matrix
	inverse = np.linalg.inv(fisher_information)

	# Equiv Check Step 1: test the design points for equality
	# step 1: make a list of discrete design points being used
	uselist = [] 
	num_unique_points = 0
	for designpt in xrange(nrow):
		if gbest_p[designpt] > 0.00001:

			c_row = np.copy(gbest_position[designpt])
			# cycle through included rows
			unique = True
			for row in xrange(num_unique_points): 
				num_same = 0
				for col in range(num_discrete+1): 
					if uselist[row][col] == c_row[col]:
						num_same += 1
				if num_same == num_discrete + 1:
					unique = False
			# end row checking for current design point
			if unique:
				uselist.append(c_row)
				num_unique_points += 1
	
	uselist = np.asmatrix(uselist)

	for designpt in xrange(nrow):
		
		# check to make sure design point being used
		if gbest_p[designpt] > 0.00001:
			
			# need to calculate wf(x)M(E)f(x) - dim
			xb = np.dot(b,gbest_position[designpt])
			w = calc_w(xb, link);
			
			# OPTIMIZE
			# now f(x)^t M(E) 
			fxM = []
			for col in xrange(dim):
				currentsum = 0
				for colit in xrange(dim):
					currentsum += gbest_position[designpt][colit] * inverse[colit][col]
				fxM.append(currentsum)
			fxM = np.asarray(fxM)
			
			# OPTIMIZE
			# now multiply by the left f(x)
			fxMfx = 0
			for col in xrange(dim):
				fxMfx += (fxM[col] * gbest_position[designpt][col])
		
			# finally multiply the expression by w and subtract the number of parameters
			check_result = (fxMfx * w) - dim
			#print "checked design point is: " + str(check_result)
			
			if check_result > threshold or check_result < -threshold:
				#print "Design not good enough because: " + str(check_result)
				# print gbest_position[designpt]
				pass_check = False
				return pass_check

	# Step 2: we want to test all other points under this design. 
	# If any are > 0 then we know design isnt optimal
	# create a matrix of possible design points for the continuous variables
	
	checkSize = 100
	if num_continuous > 0:
		testing_matrix = np.zeros((checkSize, num_continuous))
		
		for tcol in range(num_continuous): 
			increment = (ub[tcol] - lb[tcol]) / (checkSize);  # CHANGE TO CHECKSIZE
			for temp in xrange(checkSize):
				testing_matrix[temp][tcol] = lb[tcol] + (temp * increment)
		
		# test all the points
		for designpt in xrange(num_unique_points): 
			
			# create a vector to represent the new design point
			position = np.copy(uselist[designpt])
			
			# now we have created the discrete structure for the chosen design point, 
			# we next need to go through each continuous position and "do everything" to it
			# create positioning vector and populate it with zeros. Might come default to 0

			positionIndex = [0] * num_continuous
			
			# this index needs to be changed to reflect the total number done
			for designrow in xrange(-1, pow(checkSize, num_continuous)):
				# print "here"
				
				positionIndex = pointPicker(num_continuous, positionIndex, 
					num_continuous-1, checkSize-1)
				# print position
				# print testing_matrix, testing_matrix.shape
				# fill out the rest of the testing position
				for cont in range(num_continuous): 
					position[0][cont+1+num_discrete] = testing_matrix[positionIndex[cont]][cont]
				
				# calculate the interactions
				intstart = 1 + num_discrete + num_continuous
				for i in range(num_interactions):
					position[0][intstart+i] = 1 # might not need this line
					for j in range(len(interactions[i])):
						position[0][intstart+i] *= position[0][interactions[i][j]]

				# need to calculate wf(x)M(E)f(x) - dim
							# need to calculate wf(x)M(E)f(x) - dim
				b = np.reshape(b,(dim,1))
				xb = np.dot(position,b)
				xb = xb[0][0]
				# print 'xb', xb
				w = calc_w(xb, link);
				
				# now f(x)^t M(E)
				fxM = [];
				for col in xrange(dim): 
					currentsum = 0
					for colit in xrange(dim):
						currentsum += position[0][colit] * inverse[colit,col]
					fxM.append(currentsum)
				
				fxM = np.asarray(fxM)

				# OPTIMIZE
				# now multiply by the left f(x)
				fxMfx = 0;
				for col in xrange(dim): 
					fxMfx += (fxM[col] * position[0][col])
				
				# finally multiply the expression by w and subtract the number of parameters
				check_result = (fxMfx * w) - dim
				# print "checked design point is: " + str(check_result)
				
				if check_result > threshold or check_result < -threshold:
					#print "Design not good enough because: " + str(check_result)
					# print gbest_position[designpt]
					pass_check = False
					return pass_check
		# ends inclued design point loop
	# end continuous check
	return pass_check			

def duplicate_points(gbest_pos, gbest_p, dim):
	cara_num = pow(2, (dim-1))
	for comprow in xrange(cara_num):
		for row in range(comprow+1, cara_num):
			rowcomp = 0	
			for col in range(1,dim):
				rowcomp += abs(gbest_pos[comprow][col] - gbest_pos[row][col])

			if rowcomp < 0.05:
				# we need to figure out which had alarger prop allocated to it
				diff = gbest_p[comprow] - gbest_p[row]
				replace_index = row #default to replacing the lower row
				add_index = rowcomp
				if diff < 0:
					replace_index = comprow
					add_index = row
			
				# add one row to the other
				gbest_p[add_index] += gbest_p[replace_index]
				gbest_p[replace_index] = 0
	return gbest_p

def calc_delta(fisher_information, gbest_position, gbest_p, lb, ub,
	num_discrete, num_continuous, num_interactions, interactions, b,
	lower_equivalence_bound, link):
	
	dim = num_continuous + num_discrete + 1 + num_interactions
	nrow = pow(2, num_discrete+num_continuous)
	threshold = -dim * np.log(lower_equivalence_bound)
	delta = 0

	# first we need to find the inverse of the information matrix
	inverse = np.linalg.inv(fisher_information)

	# Equiv Check Step 1: test the design points for equality
	# step 1: make a list of discrete design points being used
	uselist = [] 
	num_unique_points = 0
	for designpt in xrange(nrow):
		if gbest_p[designpt] > 0.00001:

			c_row = np.copy(gbest_position[designpt])
			# cycle through included rows
			unique = True
			for row in xrange(num_unique_points): 
				num_same = 0
				for col in range(num_discrete+1): 
					if uselist[row][col] == c_row[col]:
						num_same += 1
				if num_same == num_discrete + 1:
					unique = False
			# end row checking for current design point
			if unique:
				uselist.append(c_row)
				num_unique_points += 1
	
	uselist = np.asmatrix(uselist)
	
	numpointsdes = 0;
	
	# delete below
	totalnumber = 0;
	for temp in xrange(nrow): 
		if gbest_p[temp] > 0.00001:
			totalnumber += 1

	# print "Total number of design points is: " + str(totalnumber)
	for designpt in xrange(nrow):
		
		# check to make sure design point being used
		if gbest_p[designpt] > 0.00001:
			numpointsdes += 1
			# print "Working on design point " + str(numpointsdes) 
			
			# need to calculate wf(x)M(E)f(x) - dim
			xb = np.dot(b,gbest_position[designpt])
			w = calc_w(xb, link);
			
			# OPTIMIZE
			# now f(x)^t M(E) 
			fxM = []
			for col in xrange(dim):
				currentsum = 0
				for colit in xrange(dim):
					currentsum += gbest_position[designpt][colit] * inverse[colit][col]
				fxM.append(currentsum)
			fxM = np.asarray(fxM)
			
			# OPTIMIZE
			# now multiply by the left f(x)
			fxMfx = 0
			for col in xrange(dim):
				fxMfx += (fxM[col] * gbest_position[designpt][col])
		
			# finally multiply the expression by w and subtract the number of parameters
			check_result = (fxMfx * w) - dim
			# print "checked design point is: " + str(check_result)
			
			if check_result > delta:
				# print "Design not good enough because: " + str(check_result)
				# print gbest_position[designpt]
				delta = check_result
				# print "new worst is " + str(delta)
	# Step 2: we want to test all other points under this design. 
	# If any are > 0 then we know design isnt optimal
	# create a matrix of possible design points for the continuous variables
	
	checkSize = 100
	if num_continuous > 0:
		testing_matrix = np.zeros((checkSize, num_continuous))
		
		for tcol in range(num_continuous): 
			increment = (ub[tcol] - lb[tcol]) / (checkSize);  # CHANGE TO CHECKSIZE
			for temp in xrange(checkSize):
				testing_matrix[temp][tcol] = lb[tcol] + (temp * increment)
		
		# test all the points
		for designpt in xrange(num_unique_points): 
			
			# create a vector to represent the new design point
			position = np.copy(uselist[designpt])
			
			# now we have created the discrete structure for the chosen design point, 
			# we next need to go through each continuous position and "do everything" to it
			# create positioning vector and populate it with zeros. Might come default to 0

			positionIndex = [0] * num_continuous
			
			# this index needs to be changed to reflect the total number done
			for designrow in xrange(-1, pow(checkSize, num_continuous)):
				# print "here"
				
				positionIndex = pointPicker(num_continuous, positionIndex, 
					num_continuous-1, checkSize-1)
				# print position
				# print testing_matrix, testing_matrix.shape
				# fill out the rest of the testing position
				for cont in range(num_continuous): 
					position[0][cont+1+num_discrete] = testing_matrix[positionIndex[cont]][cont]
				
				# calculate the interactions
				intstart = 1 + num_discrete + num_continuous
				for i in range(num_interactions):
					position[0][intstart+i] = 1 # might not need this line
					for j in range(len(interactions[i])):
						position[0][intstart+i] *= position[0][interactions[i][j]]

				# need to calculate wf(x)M(E)f(x) - dim
							# need to calculate wf(x)M(E)f(x) - dim
				b = np.reshape(b,(dim,1))
				xb = np.dot(position,b)
				xb = xb[0][0]
				# print 'xb', xb
				w = calc_w(xb, link);
				
				# now f(x)^t M(E)
				fxM = [];
				for col in xrange(dim): 
					currentsum = 0
					for colit in xrange(dim):
						currentsum += position[0][colit] * inverse[colit,col]
					fxM.append(currentsum)
				
				fxM = np.asarray(fxM)

				# OPTIMIZE
				# now multiply by the left f(x)
				fxMfx = 0;
				for col in xrange(dim): 
					fxMfx += (fxM[col] * position[0][col])
				
				# finally multiply the expression by w and subtract the number of parameters
				check_result = (fxMfx * w) - dim
				# print "checked design point is: " + str(check_result)
				
				if check_result > delta:
					# print "Design not good enough because: " + str(check_result)
					# print gbest_position[designpt]
					delta = check_result
					# print "new worst is " + str(delta)
		# ends inclued design point loop
	# end continuous check
	
	return delta

	
def PSO(config):
	running = True

	run = 0

	ncol = 1 + config.num_discrete + config.num_continuous + config.num_interactions
	nrow = 2 ** (config.num_discrete + config.num_continuous)

	archived_gbest_position = np.zeros((nrow, ncol)) # stores the best design found by all swarms
	archived_gbest_p = np.zeros((nrow, 1)) # best design props 
	archived_gbest = 0 # stores best determinant of info mat by all swarms
	
	
	final_gbest = 0
	final_converged = False
	final_leb = 0
	finaldes = {"design_matrix" : None, "proportions" : None}
	
	# master loop, all swarms and swarm searches happen within. Ends when max resets has been exceeded
	while running:
		
		run += 1
		
		print "Starting Run %d With current GBEST %s" % ((run, str(archived_gbest)))
		
		dim = 1 + config.num_discrete + config.num_continuous
		
		swarm = [Particle(config, name = "Particle%d" % i) for i in range(config.num_particles)]
		
		for i in range(len(swarm)):
			swarm[i].calc_fisher()
			swarm[i].calc_fitness()
		 
		gbest = calc_gbest(swarm)
		
		# code to update the global best position
		gbest_index = 0
		# declate the gbest position matrix
		gbest_position = np.zeros((nrow, ncol))
		gbest_p = np.zeros((nrow,1))

		# figure out what particle has the best position and set gbest_position to that
		for i in range(config.num_particles): 
			pbest = swarm[i].pbest
			if pbest == gbest:
				gbest_index = i
				gbest_position = swarm[i].design
				gbest_p = swarm[i].pbest_p
				gbest_p = duplicate_points(gbest_position, gbest_p, dim)
		
		iteration = 0
		converge = False
		inertia = 0.9

		# start pso loop
		while iteration < config.max_iter and converge == False:
			print "iteration ",iteration
			
			# change velocity, go to new position and find the fitness there
			for i in range(config.num_particles): 
				swarm[i].update_velocity(gbest_position, gbest_p, inertia)
				swarm[i].update_position()
				swarm[i].fix_bounds()
				swarm[i].calc_fisher()
				swarm[i].calc_fitness()
				#swarm[i].print_pbest()
			
			min_fitness = swarm[0].pbest
			for i in range(config.num_particles): 
				temppbest = swarm[i].pbest
				if temppbest > gbest:
					gbest = temppbest
					gbest_index = i
					gbest_position = swarm[i].pbest_pos
					gbest_p = swarm[i].pbest_p
					gbest_p = duplicate_points(gbest_position, gbest_p, dim)
					swarm[gbest_index].pbest_p = np.copy(gbest_p)
				
				if temppbest < min_fitness:
					min_fitness = temppbest
			
			if iteration > 40 and iteration % 20 == 0:
				
				diff = min_fitness / gbest
				
				converge = False
				converge = equivalance_check(swarm[gbest_index].fisher_info, 
				gbest_position, gbest_p,config.lb, config.ub, config.num_discrete,
				config.num_continuous, config.num_interactions, config.interactions,
				config.b, config.leb, config.link_fn_name)
				# handles a reset if the swarm already converged to the wrong design soln
				if converge == False and diff > 0.99999:
					iteration = config.max_iter
				
			# ends the iteration based equivalence check
			
			# increments the iteration
			iteration += 1
			
			# adjust the inertia
			if inertia > 0.4:
				inertia -= 0.01
			
		# Reset the entire swarm if it failed to converge to a good enough solution
		if converge == False:
			
			# see if this rounds solution was the best so far
			if gbest > archived_gbest:
				# print gbest_position
				# print gbest_p

				archived_gbest = np.copy(gbest)
				archived_gbest_position = np.copy(gbest_position)
				archived_gbest_p = np.copy(gbest_p)

			# End the search if max resets has been exceeded. Return the best archived solution
			if run > config.max_resets:
				running = False
				# print "Exceeded max resets, gbest found was: " , archived_gbest
				final_gbest = np.copy(archived_gbest)
				final_converged = False
				# finaldes = archived_gbest_position
				design_matrix = []
				# print archived_gbest_p, archived_gbest_p.shape, nrow
				for row in xrange(nrow):
					if archived_gbest_p[row] > 0.001: # FIX ME, hard-coded value
						design_matrix.append(archived_gbest_position[row])

				finaldes["design_matrix"] = np.asmatrix(design_matrix)

				# Now need to add the p_i's to finaldes
				finaldes["proportions"] = np.copy(archived_gbest_p)
				
				delta = calc_delta(swarm[gbest_index].fisher_info, gbest_position, gbest_p,
				config.lb, config.ub, config.num_discrete, config.num_continuous, 
				config.num_interactions, config.interactions,
				config.b, config.leb, config.link_fn_name)

				final_leb = math.exp(-delta / ncol)
				
		# The good ending. Swarm found right answer, spit it out to usr
		if converge == True:
			# print "The swarm has converged!"
			final_gbest = np.copy(gbest)
			final_converged = True
			finaldes = swarm[gbest_index].get_included_design()
			delta = calc_delta(swarm[gbest_index].fisher_info, gbest_position, gbest_p,
				config.lb, config.ub, config.num_discrete, config.num_continuous, 
				config.num_interactions, config.interactions, 
				config.b, config.leb, config.link_fn_name)
			
			final_leb = math.exp(-delta / ncol)
			running = False
		
		del swarm
	# end "running = True"
	
	fdes = Design() 
	fdes.gbest = final_gbest
	fdes.converged = final_converged
	fdes.finaldesign = finaldes
	fdes.leb = final_leb
	fdes.size= len(finaldes['proportions'])
	# print "Final LEB: ", final_leb
	# print "gbest is: ", final_gbest
	print "Final design:", 
	print fdes

	print finaldes

	return fdes

if __name__ == '__main__':
	from config import configs

	PSO(configs[7])