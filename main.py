from DataLoader import DataLoader
from Draw_dataset import Draw_sol
from Total_Solver import *
from VRP_Model import *
from greedy_algorithm import greedy_algorithm
from greedy_algorithm2 import greedy_algorithm2
from CFLP_Model import CFLP_Model
from CFLP_Solver import CFLP_Solver
from Solver import *
from SolutionDrawerTotal import *
#from LocalSearch import *
#import pandas as pd
from time import process_time
import glob
import sys

filename = "/dataset/coordChrist100.dat"

#Start the stopwatch / counter
t1_start = process_time()

dataset = DataLoader(path=filename)
print(filename)
print(dataset.nb_customers, dataset.nb_depots) # 20 5

#######################################################
## 1rst step - Capacitated Facility Location Problem ##
#######################################################

#### 1rst greedy algorithm
#sum_open_cost, sum_cost, facilities_isopen, facility_of_customer = greedy_algorithm(dataset.nb_depots, dataset.nb_customers, dataset.depot_capacity_list, dataset.depot_opening_costs, dataset.customer_demand_list, dataset.assignment_cost)

#### 2nd greedy algorithm
#sum_open_cost, sum_cost, facilities_isopen, facility_of_customer = greedy_algorithm2(dataset.nb_depots, dataset.nb_customers, dataset.depot_capacity_list, dataset.depot_opening_costs, dataset.customer_demand_list, dataset.assignment_cost)

#### 3rd greedy algorithm
md = CFLP_Model()
md.build_model(dataset.nb_customers, dataset.nb_depots, dataset.customer_coordinates_list, dataset.customer_demand_list, dataset.depot_coordinates_list, dataset.depot_capacity_list, dataset.depot_opening_costs)
sl = CFLP_Solver(md.customers, md.facilities, md.cost_matrix)
cflp = sl.solve()
sum_open_cost = cflp.fixed_cost
sum_cost = cflp.total_cost
facilities_isopen = cflp.facilities_isopen
facility_of_customer = cflp.facility_of_customer

print("Opening cost:", sum_open_cost)
print("Total cost of CFLP:", sum_cost)
print("Facilities status:", ' '.join([str(j) for j in facilities_isopen]))
print("The customer assignment corresponding to the facility:", ' '.join([str(j) for j in facility_of_customer]))


################################
## 2nd step - Multi-depot VRP ##
################################
routing_costs = 0
TotalNodes = []
TotalSolutions = Solution()
for facility in range(dataset.nb_depots):
    if facilities_isopen[facility] == 1:
        print("Facility:", facility)
        m = Model()
        m.BuildModel(dataset.customer_coordinates_list, dataset.depot_coordinates_list, dataset.vehicle_capacity,
                     facility, facility_of_customer, dataset.nb_customers, dataset.customer_demand_list, dataset.nb_depots,
                     dataset.route_opening_cost, dataset.is_int)
        s = Solver(m)
        sol = s.solve()
        routing_costs += sol.cost
        SolDrawer.draw(facility, sol, m.allNodes)
        TotalNodes.append(m.allNodes)
        TotalSolutions.append(sol)

t = Total_Solver(TotalSolutions, TotalNodes, dataset.route_opening_cost, dataset.is_int)
t_sol = t.solve()

print("Routing costs: ", t_sol.cost)
#print("Routing costs: ", routing_costs)
print("Opening costs:", sum_open_cost)
print("Total cost for LRP:", t_sol.cost + sum_open_cost)
#print("Total cost for LRP:", routing_costs + sum_open_cost)
SolDrawerTotal.draw('Final', TotalSolutions, TotalNodes)

# Stop the stopwatch / counter
t1_stop = process_time()

print("Elapsed time:", t1_stop, t1_start)

print("Elapsed time during the whole program in seconds:",
      t1_stop - t1_start)

print("=========================================================================================")

        #sys.stdout = sys.__stdout__