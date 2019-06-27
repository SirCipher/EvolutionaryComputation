# Following this tutorial: https://deap.readthedocs.io/en/master/tutorials/basic/part2.html

import random

from deap import base
from deap import creator
from deap import tools

IND_SIZE = 5

# Minimising two objectives fitness's
creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
# Individuals are a list of floats
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.random)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=IND_SIZE)

# Build the first individual
ind1 = toolbox.individual()

# Fitness is invalid at this point as it contains no values. This prints the base class representation,
# which has been initialised as a list
print("Individuals initial values:", ind1)


def evaluate(individual):
    a = sum(individual)
    b = len(individual)
    return a, 1. / b


ind1.fitness.values = evaluate(ind1)

# The individual is now valid as it has values associated with it
print("Fitness after evaluation:", ind1.fitness)

# Apply a gaussian mutation
mutant = toolbox.clone(ind1)
ind2, = tools.mutGaussian(mutant, mu=0.0, sigma=0.2, indpb=0.2)

# Important so that the fitness is calculated again
del mutant.fitness.values

child1, child2 = [toolbox.clone(ind1) for ind in (ind1, ind2)]

# Perform a crossover operation
tools.cxBlend(child1, child2, 0.5)

del child1.fitness.values
del child2.fitness.values

selected = tools.selBest([child1, child2], 2)
offspring = [toolbox.clone(ind) for ind in selected]
