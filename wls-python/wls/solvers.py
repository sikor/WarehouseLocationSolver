__author__ = 'pawsi_000'

import random

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

    toolbox.register("evaluate", genetic_functions.eval_individual)
    toolbox.register("mate", genetic_functions.crossover)
    toolbox.register("mutate", genetic_functions.mutate)
    toolbox.register("select", tools.   selBest)

    population = 100

    pop = toolbox.population(n=population)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, log = algorithms.eaMuCommaLambda(pop, toolbox, mu=int(population*0.25), lambda_=int(population*0.5), cxpb=0.5, mutpb=0.2, ngen=1000, stats=stats, halloffame=hof,
                                   verbose=True)



