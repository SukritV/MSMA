from population import Population
from design import Design
import numpy as np
from pso import equivalence_check, calc_delta

def MSMA(config):

	ncol = 1 + config.num_discrete + config.num_continuous + config.num_interactions
	nrow = 2 ** (config.num_discrete + config.num_continuous)

	archived_pos = np.zeros((nrow, ncol)) # stores the best design found by all populations
	archived_p = np.zeros((nrow, 1)) # best design props 
	archived_score = 0 # stores best determinant of info mat by all populations
	
	final_score = 0
	final_converged = False
	final_leb = 0
	finaldes = {"design_matrix" : None, "proportions" : None}

	# master loop, all populations and population searches happen within. 
	# ends when max resets has been exceeded

	reset = 1
	while reset <= config.max_resets:
		print "Starting Run %d With current BEST score %s" % ((reset, str(archived_score)))
		reset += 1
		
		# reset the population
		population = Population(config)
		converged = False

		iter1 = 1
		while iter1 <= config.max_iter and not converged:
			iter1 += 1
			# select parents and breed
			# mutate the children and evaluate fitness
			# select the survivers and merge
			# select individuals for stage 2
			
			if iter1 > 40 and iter1 % 20 == 0:
				converged = equivalence_check()

			iter2 = 1
			while iter2 <= config.max_iter2:
				pass

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
				config.b, config.lower_efficiency_bound, config.link)
			
			final_leb = math.exp(-delta / ncol)
			running = False
				

		# update achived design with final design
		# check equivalence theorem and calc delta on achieved design
		
	# build Design object with achieved design
	fdes = Design() 
	fdes.gbest = final_score
	fdes.converged = final_converged
	fdes.finaldesign = finaldes
	fdes.leb = final_leb

	fdes.size= True or len(finaldes['proportions']) # FIXME later
	print "Final design:", 
	print fdes
	return fdes

if __name__ == '__main__':
	from config import Config

	config = Config(num_particles=5,
		lb=[-1, -1, -1, -1],
		ub=[1, 1, 1, 1],
		max_iter=2,
		num_discrete=4,
		num_continuous=0,
		num_interactions=2,
		interactions=[(1,2), (1,3)],
		b=[0.1, 0.2, 0.3, 0.45, 0.25, 0.8, 0.4],
		max_resets=5,
		leb=0.999,
		link_fn_name="logit",

		max_iter2=5,
		mutation_prob=0.4,
		survival_rate=0.8,
		elitism_rate=0.2,
		stage2_selection_rate=0.4,
		mutation_prob2=0.4,
		survival_rate2=0.8,
		elitism_rate2=0.2)
	
	MSMA(config)