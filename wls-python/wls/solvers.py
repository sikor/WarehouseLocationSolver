__author__ = 'pawsi_000'

from wls.hierarchical import *


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


def genetic(problem: Problem, gen=100, pop=100) -> PartialMatch:
    subproblem = problem.to_subproblem()
    genetic_functions = ClientOrientedGenome(subproblem)
    return solver(subproblem, genetic_functions, pop=pop, gen=gen, verbose=True, chart=True)



def hierarchical_genetic(problem:Problem, major_pop=100, major_gen=20, minor_pop=100, minor_gen=3, major_part=None,
                         min_decrease=10, decrease_step=3) -> PartialMatch:
    if major_part is None:
        half = int(len(problem.clients)/2)
    else:
        half = major_part
    major = list(range(0, half))
    minor = list(range(half, len(problem.clients)))
    print("major: ", major, " minor: ", minor)
    subproblem = SubProblem(problem, major, minor)
    genetic_functions = HierarchicalGenome(subproblem, minor_pop, minor_gen, min_decrease=min_decrease, decrease_step=decrease_step)
    return solver(subproblem, genetic_functions, major_pop, major_gen, verbose=True, chart=True)



