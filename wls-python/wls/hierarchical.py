INFEASIBLE_PENALTY = 1000000000.0
__author__ = 'pawel'

from wls.genetic import *


class HierarchicalGenome(ClientOrientedGenome):
    def __init__(self, problem: SubProblem, minor_pop:int, minor_gen:int, decrease_step=3,
                 min_decrease=10):
        super().__init__(problem)
        self.contra_problem = SubProblem(problem.problem, problem.other_clients, problem.major_clients)
        self.minor_pop = minor_pop
        self.minor_gen = minor_gen
        self.decrease_step = decrease_step
        self.min_decrease = min_decrease

    def eval_individual(self, individual: Individual):
        individual.parent_match = None
        individual.all_match = None
        match = individual_to_partial_match(individual, self.problem)
        cost = match.get_cost()
        if cost.is_feasible:
            if self.contra_problem.clients_num() > 0:
                # print("calculating subproblem")
                all_match = solver(self.contra_problem,
                                ClientOrientedGenomeWithParent(self.contra_problem, match, self.problem),
                                pop=self.minor_pop, gen=self.minor_gen, decrease_step=self.decrease_step, min_decrease=self.min_decrease)
                full_cost = all_match.get_cost()
                individual.set_all_match(all_match)
            else:
                full_cost = cost

            if full_cost.is_feasible:
                return full_cost.total_cost,
            else:
                return INFEASIBLE_PENALTY + full_cost.overload,
        else:
            return INFEASIBLE_PENALTY + cost.overload,
