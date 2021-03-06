__author__ = 'pawsi_000'

import random
import collections

from wls.model import *

from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import matplotlib.pyplot as plt
import numpy


class Individual:
    def __init__(self, init):
        self.mapping = list()
        for i in init:
            self.mapping.append(i)

        self.parent_match = None
        self.all_match = None

    def set_parent_match(self, other_match:PartialMatch):
        self.parent_match = other_match

    def get_parent_match(self) -> PartialMatch:
        return self.parent_match

    def set_all_match(self, all_match:PartialMatch):
        self.all_match = all_match

    def get_all_match(self) -> PartialMatch:
        return self.all_match


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
creator.create("HIndividual", Individual, fitness=creator.FitnessMin)


def individual_to_partial_match(individual:Individual, problem: SubProblem):
    if individual.get_all_match() is not None:
        return individual.get_all_match()

    match = PartialMatch()
    if individual.parent_match is not None:
        match.update(individual.get_parent_match().client_to_warehouse)
    for (c, w) in enumerate(individual.mapping):
        match.assoc(problem.client(c), problem.warehouse(w))

    return match


def punish_infeasible(match:PartialMatch):
    cost = match.get_cost()
    if cost.is_feasible:
        return cost.total_cost,
    else:
        return 1000000000.0 + cost.overload,


class ClientOrientedGenome:
    def __init__(self, problem: SubProblem):
        self.problem = problem

    def eval_individual(self, individual:Individual):
        match = individual_to_partial_match(individual, self.problem)
        return punish_infeasible(match)


    def mutate(self, individual:Individual, percentage_clients):
        count = int(self.problem.clients_num() * percentage_clients)
        for x in range(count):
            index = random.randint(0, len(individual.mapping) - 1)
            individual.mapping[index] = random.randint(0, self.problem.warehouses_num() - 1)
        return individual,

    def mutate_close_open(self, individual:Individual):
        open = random.randint(0, 1)
        if open == 1:
            new_w = random.randint(0, self.problem.warehouses_num() - 1)
            for i in range(0, len(individual.mapping)):
                if random.random() < 0.25:
                    individual.mapping[i] = new_w


    def copy_warehouse(self, ind1:Individual, ind2:Individual):
        warehouse_index = random.randint(0, len(ind1.mapping) - 1)
        warehouse = ind1.mapping[warehouse_index]
        indices1 = [i for i, w in enumerate(ind1.mapping) if w == warehouse]
        for i in indices1:
            ind2.mapping[i] = warehouse

    def crossover(self, ind1, ind2):
        self.copy_warehouse(ind1, ind2)
        self.copy_warehouse(ind2, ind1)
        return ind1, ind2

    def crossover_one_point(self, ind1:Individual, ind2:Individual):
        ch1, ch2 = tools.cxOnePoint(ind1.mapping, ind2.mapping)
        ind1.mapping = ch1
        ind2.mapping = ch2
        return ind1, ind2




class ClientOrientedGenomeWithParent(ClientOrientedGenome):
    def __init__(self, problem: SubProblem, parent_match: PartialMatch, parent_problem: SubProblem):
        super().__init__(problem)
        self.parent_match = parent_match
        self.parent_problem = parent_problem

    def eval_individual(self, individual: Individual):
        individual.set_parent_match(self.parent_match)
        match = individual_to_partial_match(individual, self.problem)
        return punish_infeasible(match)


class NotDecreasingInterrupt(Exception):
    def __init__(self, min_decrease, decrease):
        self.min_decrease = min_decrease
        self.decrease = decrease

    def __str__(self):
        return "Not decreasing: %d < %d" % (self.decrease, self.min_decrease)



class GeneticInterruptor:
    def __init__(self, decrease_step, min_decrease):
        self.max_decrease = decrease_step
        self.last_values = collections.deque()
        self.min_decrease = min_decrease

    def __call__(self, data):
        cur_min = min(data)
        if len(self.last_values) == self.max_decrease:
            self.last_values.popleft()

        self.last_values.append(cur_min[0])
        decrease = self.last_values[0] - self.last_values[-1]
        if len(self.last_values) == self.max_decrease and decrease < self.min_decrease:
            raise NotDecreasingInterrupt(self.min_decrease, decrease)
        return decrease


def solver(problem: SubProblem, genetic_functions: ClientOrientedGenome, pop=100, gen=500, verbose=False,
           chart=False, min_decrease=-1000000, decrease_step=2) -> PartialMatch:
    population = pop
    toolbox = base.Toolbox()
    toolbox.register("rand_warehouse", random.randint, 0, problem.warehouses_num() - 1)
    toolbox.register("individual", tools.initRepeat, creator.HIndividual, toolbox.rand_warehouse, problem.clients_num())
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", genetic_functions.eval_individual)
    # toolbox.register("mate", genetic_functions.crossover)
    toolbox.register("mate", genetic_functions.crossover_one_point)
    # toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", genetic_functions.mutate, percentage_clients=0.05)
    #toolbox.register("mutate", tools.mutUniformInt, low=0, up=(len(problem.warehouses)-1), indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=int(population * 0.15))
    #toolbox.register("select", tools.selBest)


    pop = toolbox.population(n=population)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    stats.register("decrease", GeneticInterruptor(decrease_step=decrease_step, min_decrease=min_decrease))

    try:
        pop, log = algorithms.eaMuCommaLambda(pop, toolbox, mu=int(population * 0.3), lambda_=int(population * 0.5),
                                              cxpb=0.1, mutpb=0.8, ngen=gen, stats=stats, halloffame=hof,
                                              verbose=verbose)
    except NotDecreasingInterrupt:
        pass

    if chart:
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
        line2 = ax2.plot(gen, size_avgs, "r-", label="Average")
        ax2.set_ylabel("Average", color="r")
        for tl in ax2.get_yticklabels():
            tl.set_color("r")

        lns = line1 + line2
        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs, loc="center right")

        plt.show()

    return individual_to_partial_match(hof[0], problem)


