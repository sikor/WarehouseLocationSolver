__author__ = 'pawsi_000'

import fileinput

from wls.io import *
from wls.solvers import *

if __name__ == '__main__':
    data = read_data(fileinput.input())
    print(data)
    print(data.clients[0])
    print(data.warehouses[0])

    solution = any_fit(data)
    print(solution)