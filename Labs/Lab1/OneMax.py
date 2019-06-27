# Following tutorial https://deap.readthedocs.io/en/master/examples/ga_onemax.html

import random

from deap import base
from deap import creator
from deap import tools

# Create a new class named 'FitnessMax' that inherits from base.Fitness and give it an attribute of weights. Defines
# an optimisation problem
creator.create("FitnessMax", base.Fitness, weights=(1.0,))

# Create a new class named 'Individual' that inherits from list and set it to contain the 'FitnessMax' class in it's
# fitness attribute
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 100)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evalOneMax(individual):
    return sum(individual),


toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxUniform, indpb=0.1)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


def main():
    # Instantiate the population
    pop = toolbox.population(n=300)
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))

    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # Crossover probability
    CXPB = 0.5
    # Probability for mutating an individual
    MUTPB = 0.2

    fits = [ind.fitness.values[0] for ind in pop]
    g = 0

    while max(fits) < 100 and g < 1000:
        g = g + 1
        print("-- Generation %i --" % g)
        # Select the best individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone every individual
        offspring = list(map(toolbox.clone, offspring))

        # Extending array slicing a[start:stop:step]
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                # Set fitness invalid
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.values]
        fitnesses = map(toolbox.evaluate, invalid_ind)

        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5

        print("   Min %s" % min(fits))
        print("   Max %s" % max(fits))
        print("   Avg %s" % mean)
        print("   Std %s" % std)
        print("   Highest value:", len(max(offspring)))


if __name__ == "__main__":
    main()
