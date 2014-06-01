__author__ = 'pawsi_000'

import fileinput

from wls.io import *
from wls.solvers import *


solutions = { 'wl_16_1': 976738.625,
              'wl_25_2': 796648.4375,
              'wl_50_1': 793439.5625,
              'wl_100_4': 17765203,
              'wl_200_1': 2688,
              'wl_500_1': 2610,
              'wl_1000_1': 6073.06962,
              'wl_2000_1': 12592.17864 }


if __name__ == '__main__':
    problem = read_data(fileinput.input())
    print(problem)
    print(problem.clients[0])
    print(problem.warehouses[0])


    sol = hierarchical_genetic(problem, major_pop=20, major_part=45, major_gen=100,  minor_pop=10, minor_gen=10)
    # sol = genetic(problem)
    sol.validate(problem)

    print(sol.get_cost())

    fname = fileinput.filename().split('/')[-1]
    if fname in solutions:
        good_solution = solutions[fname]
        print("good solution:", good_solution)