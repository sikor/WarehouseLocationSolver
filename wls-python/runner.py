__author__ = 'pawsi_000'

import fileinput

from wls.io import *
from wls.solvers import *

if __name__ == '__main__':
    problem = read_data(fileinput.input())
    print(problem)
    print(problem.clients[0])
    print(problem.warehouses[0])
    print(any_fit(problem).get_cost().total_cost)
    genetic(problem)