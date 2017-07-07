

% value got from argument list is in ASCII format
arg_list = argv(); 
K = arg_list{1}; #K-value
% convert to integer
K = str2num(K);

num_discrete = str2num(arg_list{2}); % number of discrete factors
num_continuous = str2num(arg_list{3}); % number of continuous factors 
num_interaction = str2num(arg_list{4}); % number of interaction elements
disc_or_cont = 1 + str2num(arg_list{5}); % either mixed or pure discrete [0 = mixed, 1 = pure discrete]
disp(sprintf('K = %d, D = %d, C = %d, Config = %d',K,num_discrete,num_continuous,disc_or_cont));

config = getConfig(disc_or_cont,num_discrete,num_continuous,num_interaction);
best = [];


for reset=1:config.maxReset
	% reset the population
	population = createRandomPopulation(config, K);

	for iter1=1:config.maxIter1
		% stage 1 of MSMA
		population = sortPopulation(population);
		parents = selectParents(population, config, stage=1, sorted=true);
		survivers = selectSurvivers(population, config, stage=1, sorted=true);

		children = breedChildren(parents, config, stage=1);
		mutants = applyMutation(children, config, stage=1, K);
		population = mergePopulation(survivers, mutants);

		population = sortPopulation(population);
		population2 = promotedPopulation(population, config);
		disp('')
		
		for iter2=1:config.maxIter2
			% stage 2 of MSMA
			parents2 = selectParents(population2, config, stage=2, sorted=true);
			survivers2 = selectSurvivers(population2, config, stage=2, sorted=true);

			children2 = breedChildren(parents2, config, stage=2);
			mutants2 = applyMutation(children2, config, stage=2, K);
			population2 = mergePopulation(survivers2, mutants2);
			
			disp(sprintf('K = %d, Run (%d,%d,%d): fitness => %.2f', K,
				reset, iter1, iter2, overallFitness(population2)));
			best = getBestDesign(best, population2, K);
			% displayPopulation(parents2,'parents2');
			% displayPopulation(mutants2,'mutants2');
			% displayPopulation(survivers2,'survivers2');
			% displayPopulation(population2,'pop2');
		end
	end
end

disp(sprintf('\n#%.2f', best.fitness));


