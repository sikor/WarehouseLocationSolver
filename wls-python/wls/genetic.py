__author__ = 'pawsi_000'

import random

from wls.model import *


class ClientOrientedGenome:
    def __init__(self, problem: Problem):
        self.problem = problem

    def eval_individual(self, individual):
        match = PartialMatch()
        for (c, w) in enumerate(individual):
            match.assoc(self.problem.clients[c], self.problem.warehouses[w])
        cost = match.get_cost()
        if cost.is_feasible:
            return cost.total_cost,
        else:
            return 1000000000.0 + cost.overload,

    def mutate(self, individual):
        index = random.randint(0, len(individual) - 1)
        individual[index] = random.randint(0, len(self.problem.warehouses) - 1)
        return individual,

    def mutate_close_open(self, individual):
        open = random.randint(0, 1)
        if open == 1:
            new_w = random.randint(0, len(self.problem.warehouses) - 1)
            for i in range(0, len(individual)):
                if random.random() < 0.25:
                    individual[i] = new_w


    def copy_warehouse(self, ind1, ind2):
        warehouse_index = random.randint(0, len(ind1) - 1)
        warehouse = ind1[warehouse_index]
        indices1 = [i for i, w in enumerate(ind1) if w == warehouse]
        for i in indices1:
            ind2[i] = warehouse

    def crossover(self, ind1, ind2):
        self.copy_warehouse(ind1, ind2)
        self.copy_warehouse(ind2, ind1)
        return ind1, ind2

