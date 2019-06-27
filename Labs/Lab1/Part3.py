# Following tutorial https://deap.readthedocs.io/en/master/tutorials/basic/part3.html
# An extension of the One Max tutorial that adds statistics and plotting

import numpy
import random
import datetime
import matplotlib.pyplot as plt

from deap import base, algorithms
from deap import creator
from deap import tools

# Create a new class named 'FitnessMax' that inherits from base.Fitness and give it an attribute of weights. Defines
# an optimisation problem
creator.create("FitnessMax", base.Fitness, weights=(1.0,))

# Create a new class named 'Individual' that inherits from list and set it to contain the 'FitnessMax' class in it's
# fitness attribute
creator.create("Individual", list, fitness=creator.FitnessMax)

# Initialise toolbox
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

logbook = tools.Logbook()
logbook.header = "gen", "evals", "fitness", "size"
logbook.chapters["fitness"].header = "min", "avg", "max"
logbook.chapters["size"].header = "min", "avg", "max"


def main():
    # Instantiate the population
    pop = toolbox.population(n=300)
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))

    # Setup statistics
    stats_fit = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(key=len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)

    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)

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

        record = mstats.compile(pop)
        print("Stats:", record)
        logbook.record(gen=g, evals=30, **record)
        #print(logbook)

    gen = logbook.select("gen")
    fit_mins = logbook.chapters["fitness"].select("max")
    size_avgs = logbook.chapters["size"].select("avg")
    fig, ax1 = plt.subplots()
    line1 = ax1.plot(gen, fit_mins, "b-", label="Maximum Fitness")
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Fitness", color="b")
    for tl in ax1.get_yticklabels():
        tl.set_color("b")

    ax2 = ax1.twinx()
    line2 = ax2.plot(gen, size_avgs, "r-", label="Average Size")
    ax2.set_ylabel("Size", color="r")
    for tl in ax2.get_yticklabels():
        tl.set_color("r")

    lns = line1 + line2
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc="center right")

    plt.show()


if __name__ == "__main__":
    main()
