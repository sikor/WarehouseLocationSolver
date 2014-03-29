__author__ = 'pawsi_000'

from wls.model import *


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
