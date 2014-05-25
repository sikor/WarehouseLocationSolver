INFEASIBLE_PENALTY = 1000000000.0
__author__ = 'pawel'

from wls.genetic import *


class HierarchicalGenome(ClientOrientedGenome):
    def __init__(self, problem: SubProblem, minor_pop, minor_gen):
        super().__init__(problem)
        self.contra_problem = SubProblem(problem.problem, problem.other_clients, problem.major_clients)
        self.minor_pop = minor_pop
        self.minor_gen = minor_gen

    def eval_individual(self, individual: Individual):
        individual.others_match = None
        match = self.individual_to_partial_match(individual)
        cost = match.get_cost()
        if cost.is_feasible:
            if self.contra_problem.clients_num() > 0:
                others = solver(self.contra_problem,
                                ClientOrientedGenomeWithParent(self.contra_problem, individual, self.problem),
                                pop=self.minor_pop, gen=self.minor_gen)
                full_cost = others.get_cost()
            else:
                others = match
                full_cost = cost

            individual.others_match = others
            if full_cost.is_feasible:
                return full_cost.total_cost,
            else:
                return INFEASIBLE_PENALTY + full_cost.overload
        else:
            return INFEASIBLE_PENALTY + cost.overload,

    def individual_to_partial_match(self, individual:Individual, match=None, problem=None) -> PartialMatch:
        if match is None:
            match = PartialMatch()
        if individual.others_match is not None:
            match.update(individual.get_other_match().client_to_warehouse)
        else:
            super().individual_to_partial_match(individual, match)

        return match