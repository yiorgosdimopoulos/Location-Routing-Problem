import os


# Algorithm implementation
def greedy_algorithm(N, M, CAPACITY, OPEN_COST, DEMAND, ASSIGNMENT_COST):
    '''Greedy strategy
    params
    --------
    number of facilities(int)，number of customers(int)，capacity per facility(list)，opening cost(list)，
    customer demand(list)，Allocated cost per facility per customer(list[list])
    returns
    --------
    sum_cost(int): total cost
    facilities_isopen(list): facility activation
    facility_of_customer(list): facility of each customer
    '''
    # Initialization
    assignment_cost_of_facility = [0 for i in range(N)]  # Allocated cost per facility
    facility_of_customer = [0 for i in range(M)]  # clients assigned to each facility
    residual_capacity = CAPACITY.copy()  # Remaining capacity of all facilities
    facilities_isopen = [0 for i in range(N)]  # Whether the facility is turned on，1:open, 2: close

    # Iterate over all customers
    for customer in range(M):
        # Acquire the facility with the lowest allocated cost available

        # A list of optional facilities, sorted, from low to high[(i,v),...]
        opt_facilities = sorted(enumerate(ASSIGNMENT_COST[customer]), key=lambda x: x[1])
        for facility, cost in opt_facilities:
            if residual_capacity[facility] >= DEMAND[customer]:  # If the remaining capacity of the facility is sufficient
                assignment_cost_of_facility[facility] += cost
                residual_capacity[facility] -= DEMAND[customer]  # Update the remaining capacity of the facility
                # facility_of_customer[facility].append(customer) # Update the assigned client for each facility
                facility_of_customer[customer] = facility
                if facilities_isopen[facility] == 0:
                    facilities_isopen[facility] = 1
                break
            else:
                pass

    # total cost
    sum_cost = 0
    for facility in range(N):
        # Opening cost
        open_cost_n = facilities_isopen[facility] * OPEN_COST[facility]
        # Assignment cost
        assignment_cost_n = assignment_cost_of_facility[facility]
        # Total cost
        sum_cost += open_cost_n + assignment_cost_n

    sum_open_cost = 0
    sum_assignment_cost = 0
    for facility in range(N):
        # Opening cost
        sum_open_cost += facilities_isopen[facility] * OPEN_COST[facility]
        # Assignment cost
        sum_assignment_cost += assignment_cost_of_facility[facility]

    return sum_open_cost, sum_cost, facilities_isopen, facility_of_customer