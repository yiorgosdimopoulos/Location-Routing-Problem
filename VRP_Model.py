import random
import math

#from main import *
from DataLoader import *


class Model:

    # instance variables
    def __init__(self):
        self.allNodes = []
        self.customers = []
        self.matrix = []
        self.capacity = -1
        self.cost = -1

    def BuildModel(self, customer_coordinates_list=None, depot_coordinates_list=None, vehicle_capacity=None, facility=None,
                   facility_of_customer: object = None, nb_customers=None, customer_demand_list=None, nb_depots=None,
                   route_opening_cost=None, is_int=None):

        depot = Node(0, facility, depot_coordinates_list[facility][0], depot_coordinates_list[facility][1], 0)
        self.allNodes.append(depot)
        self.capacity = vehicle_capacity
        self.cost = route_opening_cost
        self.is_int = is_int

        k = 1
        l = nb_depots + 1
        for customer in range(nb_customers):
            if facility_of_customer[customer] == facility:
                xx = customer_coordinates_list[customer][0]
                yy = customer_coordinates_list[customer][1]
                dem = customer_demand_list[customer]
                cust = Node(k, customer + l, xx, yy, dem)
                k += 1
                self.allNodes.append(cust)
                self.customers.append(cust)

        rows = len(self.allNodes)
        self.matrix = [[0.0 for x in range(rows)] for y in range(rows)]

        for i in range(0, len(self.allNodes)):
            for j in range(0, len(self.allNodes)):
                a = self.allNodes[i]
                b = self.allNodes[j]
                dist = math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
                if self.is_int == False:
                    dist = dist * 100
                self.matrix[i][j] = dist

class Node:
    def __init__(self, idd, pos, xx, yy, dem):
        self.x = xx
        self.y = yy
        self.ID = idd
        self.position = pos
        self.demand = dem
        self.isRouted = False


class Route:
    def __init__(self, dp, cap, cos):
        self.sequenceOfNodes = []
        self.sequenceOfNodes.append(dp)
        self.sequenceOfNodes.append(dp)
        self.cost = cos
        self.capacity = cap
        self.load = 0