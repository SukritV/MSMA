from individual import Individual
import numpy as np, copy

class MSMAException(Exception):
	pass

class Population:
	def __init__(self, config, population=[]):
		self.population = population
		self.fitness_evaluated = False
		if population == []:
			for _ in xrange(config.num_particles):
				self.population.append(Individual(config))			
		
	def __len__(self):
		return len(self.population)

	def __repr__(self):
		return 'Population(size=%d\n' % len(self) +\
			'\n'.join([str(person.name) + ' fitness=' + str(person.fitness)
				for person in self.population]) + ')\n'

	def __getitem__(self, index):
		return self.population[index]

	def evaluate_fitness(self):
		if self.fitness_evaluated:
			return
		else:
			for i in xrange(len(self.population)):
				self.population[i].calc_fitness()
			self.fitness_evaluated = True

		self.sort()

	@classmethod
	def generate(self, config, pop_size):
		'randomly generates num_individuals and returns population'
		population = []
		for _ in xrange(pop_size):
			population.append(Individual(config))
		return Population(config, population=population)

	def select(self, num_selected):
		if not self.fitness_evaluated:
			self.evaluate_fitness()
		return Population(config,
			population=copy.deepcopy(self.population[:num_selected]))

	def select_elites(self, elitism_rate):
		if elitism_rate > 1 or elitism_rate < 0:
			raise MSMAException('Invalid elitism_rate %g' % elitism_rate + \
				', must be between 0 and 1 inclusive.')
		num_elites = int(len(self) * elitism_rate)
		return self.select(num_elites)

	def select_survivers(self, survival_rate):
		if survival_rate > 1 or survival_rate < 0:
			raise MSMAException('Invalid survival_rate %g' % elitism_rate + \
				', must be between 0 and 1 inclusive.')
		num_survivers = int(len(self) * survival_rate)
		return self.select(num_survivers)
	
	def select_best_individual(self):
		return self.select(1)[0]

	def merge(self, other):
		return Population(population=self.population+other.population)

	def sort(self):
		self.population = list(reversed(sorted(self.population, 
			key = lambda x: x.fitness)))

if __name__ == '__main__':
	from config import Config 

	config = Config(num_discrete=2, num_continuous=3, num_interactions=2, 
		interactions=[(1,2),(3,3)], b=np.random.random(8).tolist(), 
		lb=[-1,-2,-1,-2,-3], ub=[1,2,1,2,3],
		max_iter=10, num_particles=25, link_fn_name="logit")
	print config
	pop = Population(config)
	print pop
	pop.evaluate_fitness()
	print pop
	pop2 = Population.generate(config,10)
	print pop2
	pop2.evaluate_fitness()
	print pop2
	pop3 = pop2.select(5)
	print pop3