__author__ = 'pawsi_000'

import random

import matplotlib.pyplot as plt
import numpy
from deap import base
from deap import creator
from deap import tools
from deap import algorithms

from wls.genetic import *


def any_fit(problem: Problem) -> PartialMatch:
    match = PartialMatch()
    warehouses_it = problem.warehouses_it()
    current_warehouse = next(warehouses_it)
    for client in problem.clients_by_demand_desc():
        if not match.can_serve(current_warehouse, client):
            try:
                current_warehouse = next(warehouses_it)
            except StopIteration:
                current_warehouse = match.most_free_warehouse()
        match.assoc(client, current_warehouse)

    return match


def genetic(problem: Problem) -> PartialMatch:
    creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("rand_warehouse", random.randint, 0, len(problem.warehouses) - 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.rand_warehouse, len(problem.clients))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    genetic_functions = ClientOrientedGenome(problem)
    
    population = 100

    toolbox.register("evaluate", genetic_functions.eval_individual)
    #toolbox.register("mate", genetic_functions.crossover)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", genetic_functions.mutate, percentage_clients=0.05)
    #toolbox.register("mutate", tools.mutUniformInt, low=0, up=(len(problem.warehouses)-1), indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize = int(population*0.15))
    #toolbox.register("select", tools.selBest)

    pop = toolbox.population(n=population)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, log = algorithms.eaMuCommaLambda(pop, toolbox, mu=int(population*0.3), lambda_=int(population*0.5), cxpb=0.1, mutpb=0.8, ngen=500, stats=stats, halloffame=hof,
                                   verbose=True)


    gen = log.select("gen")
    fit_mins = log.select("min")
    size_avgs = log.select("avg")
    #print (fit_mins, " ", size_avgs)
    fig, ax1 = plt.subplots()
    line1 = ax1.plot(gen, fit_mins, "b-", label="Minimum Fitness")
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



