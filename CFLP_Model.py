import math

class Facility:
    def __init__(self, id, x, y, capacity, opening_cost):
        self.id = id
        self.capacity = capacity
        self.opening_cost = opening_cost
        self.assigned_customers = []
        self.x = x
        self.y = y
        self.total_demand = 0
        self.comb_cost = 0
 #       self.facilities_isopen = []

class Customer:
    def __init__(self, id, x, y, demand):
        self.id = id
        self.assigned_to_facility_id = None
        self.x = x
        self.y = y
        self.demand = demand
        self.tabu_iterator = -1


class CFLP_Model:
    def __init__(self):
        self.facilities = []
        self.customers = []
        self.cost_matrix = []


    def build_model(self, custs, facilities, customer_coordinates_list, customer_demand_list, depot_coordinates_list, depot_capacity_list, depot_opening_costs):
        for i in range (custs):
            x = customer_coordinates_list[i][0]
            y = customer_coordinates_list[i][1]
            demand = customer_demand_list[i]
            c = Customer(i, x, y, demand)
            self.customers.append(c)

        for j in range(facilities):
            x = depot_coordinates_list[j][0]
            y = depot_coordinates_list[j][1]
            capacity = depot_capacity_list[j]
            opening_cost = depot_opening_costs[j]
            f = Facility(j, x, y, capacity, opening_cost)
            self.facilities.append(f)

        self.cost_matrix = [[0.0 for j in range(len(self.facilities))] for i in range(len(self.customers))]

        for c in self.customers:
            c:Customer
            for f in self.facilities:
                f:Facility
                distance = math.sqrt(math.pow(c.x - f.x, 2) + math.pow(c.y - f.y, 2))
                cost = (distance * c.demand) / 1000
                self.cost_matrix[c.id][f.id] = cost





