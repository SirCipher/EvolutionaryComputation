import random
import operator
import csv
import itertools
import pygraphviz as pgv

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp


with open("spambase.csv") as spambase:
    spamReader = csv.reader(spambase)
    spam = list(list(float(elem) for elem in row) for row in spamReader)

pset = gp.PrimitiveSetTyped("MAIN", itertools.repeat(float, 57), bool, "IN")

pset.addPrimitive(operator.and_, [bool, bool], bool)
pset.addPrimitive(operator.or_, [bool, bool], bool)
pset.addPrimitive(operator.not_, [bool], bool)


def protectedDiv(left, right):
    try: return left / right
    except ZeroDivisionError: return 1


pset.addPrimitive(operator.add, [float,float], float)
pset.addPrimitive(operator.sub, [float,float], float)
pset.addPrimitive(operator.mul, [float,float], float)
pset.addPrimitive(protectedDiv, [float,float], float)


def if_then_else(input, output1, output2):
    if input: return output1
    else: return output2


pset.addPrimitive(operator.lt, [float, float], bool)
pset.addPrimitive(operator.eq, [float, float], bool)
pset.addPrimitive(if_then_else, [bool, float, float], float)

pset.addEphemeralConstant("rand100", lambda: random.random() * 100, float)
pset.addTerminal(False, bool)
pset.addTerminal(True, bool)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)


def evalSpambase(individual):
    func = toolbox.compile(expr=individual)

    length = len(spam)
    max = int(0.8 * length)

    spam_samp = random.sample(spam[:max:], 400)
    result = sum(bool(func(*mail[:57])) is bool(mail[57]) for mail in spam_samp)
    return result,


toolbox.register("evaluate", evalSpambase)
toolbox.register("select", tools.selTournament, tournsize=5)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=1, max_=4)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))


def main():
    random.seed(50)
    pop = toolbox.population(n=50)
    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    algorithms.eaSimple(pop, toolbox, 0.5, 0.2, 50, stats, halloffame=hof)

    expr = tools.selBest(pop, 1)[0]
    nodes, edges, labels = gp.graph(expr)

    print(expr)

    g = pgv.AGraph(nodeSep=1.0)
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    g.layout(prog="dot")

    for	i in nodes:
        n = g.get_node(i)
        n.attr["label"]	= labels[i]

    g.draw("tree.pdf")

    func = toolbox.compile(expr=expr)

    correct = 0
    length = len(spam)
    max = int(0.2 * length)
    print(max)

    for mail in spam[:max:]:
        result = bool(func(*mail[:57]))
        actual = bool(mail[57])

        if(result == actual):
            correct += 1


    length = len(spam)
    print("Length %s " % length)
    print("Correct %s" % correct)

    print((correct/float(length))*100)


if __name__ == "__main__":
    main()
