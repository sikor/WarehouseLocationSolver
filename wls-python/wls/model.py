__author__ = 'pawsi_000'


class Warehouse:
    def __init__(self, wid, cap, setup):
        self.cap = int(cap)
        self.setup = float(setup)
        self.wid = int(wid)

    def __repr__(self):
        return "Warehouse(id=" + str(self.wid) + ", cap=" + str(self.cap) + ", setup=" + str(self.setup) + ")"

    def __hash__(self):
        return self.wid.__hash__()

    def __eq__(self, other):
        return self.wid.__eq__(other)


class Client:
    def __init__(self, cid, dem, cost):
        self.dem = int(dem)
        self.cost = [float(x) for x in cost]
        self.cid = int(cid)

    def __repr__(self):
        return "Client(id=" + str(self.cid) + ", dem=" + str(self.dem) + ", costs=" + str(sum(self.cost)) + ")"

    def __hash__(self):
        return self.cid.__hash__()

    def __eq__(self, other):
        return self.cid.__eq__(other)


class Problem:
    def __init__(self, warehouses, clients):
        self.clients = dict()
        self.warehouses = dict()
        for client in clients:
            self.clients[client.cid] = client
        for warehouse in warehouses:
            self.warehouses[warehouse.wid] = warehouse

        self.total_capacity = sum(map(lambda w: w.cap, warehouses))
        self.total_demand = sum(map(lambda c: c.dem, clients))

    def __repr__(self):
        return "Problem(w=" + str(len(self.warehouses)) + ", c=" + str(len(self.clients)) \
               + ", total_cap=" + str(self.total_capacity) + ", total_demand=" + str(self.total_demand) + ")"

    def warehouses_it(self):
        return iter(self.warehouses.values())

    def clients_by_demand_desc(self):
        return sorted(self.clients.values(), key=lambda c: c.dem, reverse=True)


class PartialMatch:
    def __init__(self):
        self.client_to_warehouse = dict()
        self.warehouse_to_clients = dict()
        self.free_cap = dict()

    def assoc(self, client: Client, warehouse: Warehouse):
        self.client_to_warehouse[client] = warehouse
        if warehouse in self.warehouse_to_clients:
            self.warehouse_to_clients[warehouse].append(client)
        else:
            self.warehouse_to_clients[warehouse] = [client]
        self.free_cap[warehouse] = self.free_cap.get(warehouse, warehouse.cap) - client.dem

    def can_serve(self, current_warehouse: Warehouse, client: Client):
        return self.free_cap.get(current_warehouse, current_warehouse.cap) >= client.dem

    def most_free_warehouse(self):
        key, value = min(self.free_cap.items(), key=lambda i: i[1])
        return key

    def get_cost(self):
        pass

    def __repr__(self):
        return str(self.client_to_warehouse)


