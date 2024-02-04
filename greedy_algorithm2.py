import os


# Algorithm implementation
def greedy_algorithm2(N, M, CAPACITY, OPEN_COST, DEMAND, ASSIGNMENT_COST):
    '''Greedy strategy 2
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
        # A list of optional facilites, sorted, from low to high[(i,v),...]
        opt_facilities = sorted(enumerate(ASSIGNMENT_COST[customer]), key=lambda x: x[1])
        open_facility = None
        close_facility = None
        final_facility = None
        for facility, cost in opt_facilities:  # Opened and unopened facilities that get the minimum allocated cost
            if open_facility != None and close_facility != None:
                break
            if residual_capacity[facility] >= DEMAND[customer]:
                if facilities_isopen[facility] == 1:
                    if open_facility == None:
                        open_facility = facility
                else:
                    if close_facility == None:
                        close_facility = facility

        # opened
        if open_facility != None and close_facility == None:
            final_facility = open_facility
        # unopened
        elif open_facility == None and close_facility != None:
            final_facility = close_facility
            facilities_isopen[final_facility] = 1  # renew
        # If both exist, choose the one with the lowest total cost
        else:
            if OPEN_COST[close_facility] + ASSIGNMENT_COST[customer][close_facility] >= ASSIGNMENT_COST[customer][open_facility]:
                final_facility = open_facility
            else:
                final_facility = close_facility
                facilities_isopen[final_facility] = 1  # renew

        # renew
        assignment_cost_of_facility[final_facility] += ASSIGNMENT_COST[customer][final_facility]
        residual_capacity[final_facility] -= DEMAND[customer]  # Update the remaining capacity of the facility
        facility_of_customer[customer] = final_facility

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