import operator
import math
import random
import numpy
import pygraphviz as pgvusing

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

data = numpy.genfromtxt('training.csv', delimiter=",")


def protectedDiv(left, right):
    if right == 0:
        right = 1

    return left / right


pset = gp.PrimitiveSet("MAIN", 4)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(protectedDiv, 2)
pset.addPrimitive(operator.neg, 1)
pset.addEphemeralConstant("rand101", lambda: random.randrange(-1, 1))

pset.renameArguments(ARG0='Column1')
pset.renameArguments(ARG1='Column2')
pset.renameArguments(ARG2='Column3')
pset.renameArguments(ARG3='Column4')

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=2, max_=4)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)


def evalMeanSquDiff(individual):
    func = toolbox.compile(expr=individual)
    totalSquDiff = sum((func(row[0], row[1], row[2], row[3]) - row[4]) ** 2 for row in data)

    return totalSquDiff / len(data),


toolbox.register("evaluate", evalMeanSquDiff)
toolbox.register("select", tools.selTournament, tournsize=10)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genGrow, min_=0, max_=3)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))


def main():
    print('-------------------------------------------------------------------------------')
    print('Training...')
    random.seed(256)

    pop = toolbox.population(n=50)
    hof = tools.HallOfFame(5)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)

    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)

    pop, log = algorithms.eaSimple(pop, toolbox, 0.8, 0.2, 50, stats=mstats, halloffame=hof, verbose=True)

    best = hof.__getitem__(0)
    print(best)

    func = toolbox.compile(expr=best)
    expr = tools.selBest(pop, 1)[0]
    nodes, edges, labels = gp.graph(expr)

    # Plot the tree
    g = pgv.AGraph(nodeSep=1.0)
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    g.layout(prog="dot")

    for	i in nodes:
        n = g.get_node(i)
        n.attr["label"]	= [i]

    g.draw("tree.pdf")

    print('-------------------------------------------------------------------------------')
    print('Testing...')
    print(''.join(row.ljust(15) for row in ['Row', 'Predicted', 'Actual', 'Error']))

    i = 0

    for row in numpy.genfromtxt('testing.csv', delimiter=","):
        result = func(row[0], row[1], row[2], row[3])
        actual = row[4]
        diff = (100 * abs((result - actual)) / actual)

        i += 1
        result = '%f' % result
        actual = '%f' % actual
        diff = '%.3f%%' % diff

        print(''.join(row.ljust(15) for row in [str(i), result, actual, diff]))

    return pop, log, hof


if __name__ == "__main__":
    main()
