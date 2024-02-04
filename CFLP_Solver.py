from CFLP_Model import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

class Solution():
    def __init__(self, facilities, cost, fixed_cost_component, operating_cost_component, facilities_isopen, facility_of_customer):
        self.facilities = facilities.copy()
        for i in range(len(facilities)):
            self.facilities[i].assigned_customers = facilities[i].assigned_customers.copy()

        self.total_cost = cost
        self.operating_cost = operating_cost_component
        self.fixed_cost = fixed_cost_component
        self.facilities_isopen = facilities_isopen
        self.facility_of_customer = facility_of_customer


class CFLP_Solver:
    def __init__(self, customers, facilities, cost_matrix):
        self.customers = customers
        self.facilities = facilities
        self.cost_matrix = cost_matrix
        self.cost = 0
        self.fixed_cost_component = 0
        self.operating_cost_component = 0
        self.sol = None

    def calculate_cost(self, sol_to_test=None):
        fixed_cost = 0
        operating_cost = 0

        if sol_to_test is None:
            for f in self.facilities:
                f: Facility
                if len(f.assigned_customers) > 0:
                    fixed_cost += f.opening_cost
                    for c in f.assigned_customers:
                        operating_cost += self.cost_matrix[c.id][f.id]
            # print('testing', fixed_cost, operating_cost)
            tot_cost = fixed_cost + operating_cost
        else:
            for f in sol_to_test.facilities:
                f: Facility
                if len(f.assigned_customers) > 0:
                    fixed_cost += f.opening_cost
                    for c in f.assigned_customers:
                        operating_cost += self.cost_matrix[c.id][f.id]
            # print('testing', fixed_cost, operating_cost)
            tot_cost = fixed_cost + operating_cost
        return tot_cost

    def initialize_everything(self):
        self.cost = 0
        self.fixed_cost_component = 0
        self.operating_cost_component = 0
        for f in self.facilities:
            f: Facility
            f.assigned_customers.clear()
            f.total_demand = 0
        for c in self.customers:
            c: Customer
            c.assigned_to_facility_id = None

    def draw_solution(self, sol_to_draw=None):
        if sol_to_draw is None:
            for f in self.facilities:
                # plt.clf()
                if len(f.assigned_customers) > 0:
                    plt.plot(f.x, f.y, marker='s', markersize=6)
                else:
                    plt.plot(f.x, f.y, marker='x', markersize=4)
                for c in f.assigned_customers:
                    plt.plot([f.x, c.x], [f.y, c.y], linewidth = 0.5)
            plt.title("Total Cost " + str(self.cost))
        else:
            for f in sol_to_draw.facilities:
                # plt.clf()
                if len(f.assigned_customers) > 0:
                    plt.plot(f.x, f.y, marker='s', markersize=6)
                else:
                    plt.plot(f.x, f.y, marker='x', markersize=4)
                for c in f.assigned_customers:
                    plt.plot([f.x, c.x], [f.y, c.y], linewidth = 0.5)
            plt.title("Total Cost " + str(sol_to_draw.total_cost))
        plt.show()

    def initial_solution_cheapest_insertion(self):
        self.initialize_everything()
        for ins in range(0, len(self.customers)):
            print(ins)
            best_so_far = math.pow(10, 10)
            best_cust_id = None
            best_facility_id = None
            best_fixed = math.pow(10, 10)
            best_operating = math.pow(10, 10)
            for i in range(0, len(self.customers)):
                trial_customer: Customer = self.customers[i]
                if trial_customer.assigned_to_facility_id is not None:
                    continue

                for j in range(0, len(self.facilities)):
                    trial_facility: Facility = self.facilities[j]

                    if trial_facility.total_demand + trial_customer.demand > trial_facility.capacity:
                        continue

                    fixed_cost = 0
                    if len(trial_facility.assigned_customers) == 0:
                        fixed_cost = trial_facility.opening_cost

                    trial_cost = fixed_cost + self.cost_matrix[trial_customer.id][trial_facility.id]

                    if trial_cost < best_so_far:
                        # if cost_matrix[trial_customer.id][trial_facility.id] < best_operating:
                        best_cust_id = i
                        best_facility_id = j
                        best_fixed = fixed_cost
                        best_operating = self.cost_matrix[trial_customer.id][trial_facility.id]
                        best_so_far = trial_cost

            if best_cust_id is not None:
                ins_customer: Customer = self.customers[best_cust_id]
                ins_facility: Facility = self.facilities[best_facility_id]
                ins_facility.assigned_customers.append(ins_customer)
                ins_facility.total_demand += ins_customer.demand
                ins_customer.assigned_to_facility_id = ins_facility.id
                self.cost += best_so_far
                self.fixed_cost_component += best_fixed
                self.operating_cost_component += best_operating
        self.test_and_draw()

    def sort_candidate_facilities(self, candidate_facilities, set_unassigned_customers):
        for f in self.facilities:
            f: Facility
            avg_cost = 0
            for c in set_unassigned_customers:
                avg_cost += self.cost_matrix[c.id][f.id]
            avg_cost = avg_cost / len(set_unassigned_customers)
            # f.comb_cost = (avg_cost * f.opening_cost) / f.capacity
            f.comb_cost = f.opening_cost / f.capacity
        candidate_facilities.sort(key=lambda x: x.comb_cost)

    def test_and_draw(self, sol_to_test=None):
        if sol_to_test is None:
            test_sol = self.calculate_cost()
            if abs(self.cost - test_sol) > 0.001:
                print('error')
            self.draw_solution()
            print('Total cost', self.cost, 'Fixed cost', self.fixed_cost_component, 'Operating cost',
                  self.operating_cost_component)
        else:
            test_sol = self.calculate_cost(sol_to_test)
            if abs(self.cost - test_sol) > 0.001:
                print('error')
            self.draw_solution(sol_to_test)
            print('Total cost', self.cost, 'Fixed cost', self.fixed_cost_component, 'Operating cost',
                  self.operating_cost_component)

    def test(self):
        test_sol = self.calculate_cost()
        if abs(self.cost - test_sol) > 0.001:
            print('error')
        # print('Total cost', self.cost)
        # print('Fixed cost', self.fixed_cost_component)
        # print('Operating cost', self.operating_cost_component)

    # comparable fixed and variable costs
    def cheapest_facilities_first(self):
        self.initialize_everything()
        set_unassigned_customers = set(self.customers)
        candidate_facilities = self.facilities.copy()
        self.sort_candidate_facilities(candidate_facilities, set_unassigned_customers)

        while len(set_unassigned_customers) > 0:
            f: Facility = candidate_facilities.pop(0)
            self.fixed_cost_component += f.opening_cost
            f.candidate_customers = [c for c in set_unassigned_customers]
            f.candidate_customers.sort(key=lambda c: self.cost_matrix[c.id][f.id])
            print(len(set_unassigned_customers))
            # test_and_draw(facilities, customers, cost_matrix, cost, fixed_cost_component, operating_cost_component)
            for c in f.candidate_customers:
                c: Customer
                if f.total_demand + c.demand > f.capacity:
                    continue
                f.assigned_customers.append(c)
                f.total_demand += c.demand
                set_unassigned_customers.remove(c)
                self.operating_cost_component += self.cost_matrix[c.id][f.id]
            if len(set_unassigned_customers) > 0:
                self.sort_candidate_facilities(candidate_facilities, set_unassigned_customers)
        self.cost = self.fixed_cost_component + self.operating_cost_component
        self.test_and_draw()

    # comparable fixed and variable costs
    def batches_of_facilities(self):
        self.initialize_everything()
        facilities_isopen = [0 for i in self.facilities]
        facility_of_customer = [0 for i in self.customers]
        set_unassigned_customers = set(self.customers)
        candidate_facilities = self.facilities.copy()
        self.sort_candidate_facilities(candidate_facilities, set_unassigned_customers)

        while len(set_unassigned_customers) > 0:
            facilities_to_be_used = self.facilities_needed_for_unassigned(candidate_facilities,
                                                                          set_unassigned_customers)
            while True:
                selected_facility, selected_customer = self.find_best_assignment_pair(facilities_to_be_used,
                                                                                      set_unassigned_customers)
                if selected_facility is None:
                    break
                if len(selected_facility.assigned_customers) == 0:
                    self.fixed_cost_component += selected_facility.opening_cost
                selected_facility.assigned_customers.append(selected_customer)
                selected_facility.total_demand += selected_customer.demand
                set_unassigned_customers.remove(selected_customer)
                selected_customer.assigned_to_facility_id = selected_facility.id
                self.operating_cost_component += self.cost_matrix[selected_customer.id][selected_facility.id]
                if len(set_unassigned_customers) > 0:
                    self.sort_candidate_facilities(candidate_facilities, set_unassigned_customers)

        self.cost = self.fixed_cost_component + self.operating_cost_component
        for f in self.facilities:
            if len(f.assigned_customers) > 0:
                facilities_isopen[f.id] = 1
            else:
                facilities_isopen[f.id] = 0
        for c in self.customers:
            facility_of_customer[c.id] = c.assigned_to_facility_id
        self.sol = Solution(self.facilities, self.cost, self.fixed_cost_component, self.operating_cost_component, facilities_isopen, facility_of_customer)
        self.test_and_draw()

    def solve(self):
        self.construction_heuristic()
        return self.sol

    def facilities_needed_for_unassigned(self, candidate_facilities: list, set_unassigned_customers):
        total_load_unassigned = sum(c.demand for c in set_unassigned_customers)
        tot_load = 0
        selected_facilities = []
        for f in candidate_facilities:
            tot_load += f.capacity
            selected_facilities.append(f)
            if tot_load >= total_load_unassigned:
                break
        for f in selected_facilities:
            candidate_facilities.remove(f)

        return selected_facilities

    def find_best_assignment_pair(self, facilities_to_be_used, set_unassigned_customers):
        bst = 10 ** 10
        bst_f = None
        bst_c = None

        for c in set_unassigned_customers:
            c: Customer
            for f in facilities_to_be_used:
                f: Facility
                if f.total_demand + c.demand <= f.capacity:
                    if self.cost_matrix[c.id][f.id] < bst:
                        bst = self.cost_matrix[c.id][f.id]
                        bst_c = c
                        bst_f = f
        return bst_f, bst_c

    def construction_heuristic(self):
        # self.initial_solution_cheapest_insertion()
        # self.cheapest_facilities_first()
        self.batches_of_facilities()

