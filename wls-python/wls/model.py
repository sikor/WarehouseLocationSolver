__author__ = 'pawsi_000'


class Warehouse:
    def __init__(self, wid, cap, setup):
        self.cap = int(cap)
        self.setup = float(setup)
        self.wid = int(wid)

    def __repr__(self):
        return "Warehouse(id=" + str(self.wid) + ", cap=" + str(self.cap) + ", setup=" + str(self.setup) + ")"


class Client:
    def __init__(self, cid, dem, cost):
        self.dem = int(dem)
        self.cost = [float(x) for x in cost]
        self.cid = int(cid)

    def __repr__(self):
        return "Client(id=" + str(self.cid) + ", dem=" + str(self.dem) + ", costs=" + str(self.cost) + ")"


class Problem:
    def __init__(self, warehouses, clients):
        self.warehouses = warehouses
        self.clients = clients

    def __repr__(self):
        return "Problem(w=" + str(len(self.warehouses)) + ", c=" + str(len(self.clients)) + ")"
