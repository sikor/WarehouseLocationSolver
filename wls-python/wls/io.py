__author__ = 'pawsi_000'

from wls.model import *


def read_data(input_stream):
    (w, c) = input_stream.readline().split(" ") #W - number of Warehouses, C-number of clients
    (w, c) = (int(w), int(c))
    wareshouses = list()
    clients = list()
    for i in range(0, w):
        (cap, setup) = input_stream.readline().split(" ")
        wareshouses.append(Warehouse(i, cap, setup))
    for i in range(0, c):
        d = input_stream.readline()
        cost = input_stream.readline().split(" ")
        if len(cost) != w:
            raise Exception(
                "Number of costs in client(%d) %d is different than number of warehouses %d" % (i, len(cost), w))
        clients.append(Client(i, d, cost))
    return Problem(wareshouses, clients)