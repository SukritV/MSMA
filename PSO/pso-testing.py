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
		link_fn_name="logit")

from numpy import random as rd
#rand in python is [0,1), Matlab is (0,1)
num_particles = [25,50,100,150]

lb
ub

max_iter = [100,150,300]
num_discrete = [0,1,2,3,4,5,6,7,8]
num_continuous = 8 - num discrete
num_interactions = 0
interactions = []
b = -3 to +3
max_rests = [50,100]
leb = 0.99
link_fn_name = ["logit", "probit", "loglog", "cloglog"]