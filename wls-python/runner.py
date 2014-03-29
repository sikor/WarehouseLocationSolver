__author__ = 'pawsi_000'

import fileinput

from wls.io import *


if __name__ == '__main__':
    data = read_data(fileinput.input())
    print(data)
    print(data.clients[0])
    print(data.warehouses[0])