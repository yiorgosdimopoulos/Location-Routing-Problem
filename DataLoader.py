import math

class DataLoader:
    NB_CUSTOMERS_LINE = 0
    NB_DEPOTS_LINE = 1

    def __init__(self, path):
        self.path = path
        self.nb_customers = 0
        self.nb_depots = 0

        self.customer_coordinates_list = list()
        self.depot_coordinates_list = list()

        self.vehicle_capacity = 0

        self.depot_capacity_list = list()

        self.customer_demand_list = list()

        self.depot_opening_costs = list()

        self.route_opening_cost = 0

        self.assignment_cost = []

        self.OFFSET = 0

        self.is_int = None

        self._load_dataset()

        self._find_assignment_costs()

    def next_offset(self, n=1):
        self.OFFSET += n

    def _load_depot_capacities(self, lines: list):
        START = self.OFFSET
        END = self.OFFSET + self.nb_depots

        self.depot_capacity_list = list(map(int, lines[START: END]))

        self.next_offset(self.nb_depots)

    def _load_depot_coordinates(self, lines: list):
        START = self.OFFSET
        END = self.OFFSET + self.nb_depots

        for line in lines[START: END]:
            line = line.split(' ')
            line = list(filter(lambda l: l != '', line))
            x = int(line[0])
            y = int(line[1])
            self.depot_coordinates_list.append((x, y))

        self.next_offset(self.nb_depots)

    def _load_customer_coordinates(self, lines: list):
        START = self.OFFSET
        END = self.OFFSET + self.nb_customers

        for line in lines[START: END]:
            line = line.split(' ')
            line = list(filter(lambda l: l != '', line))
            x = int(line[0])
            y = int(line[1])
            self.customer_coordinates_list.append((x, y))

        self.next_offset(self.nb_customers)

    def _load_customer_demands(self, lines: list):
        START = self.OFFSET
        END = self.OFFSET + self.nb_customers
        self.customer_demand_list = list(map(int, lines[START: END]))

        self.next_offset(self.nb_customers)

    def _load_depot_opening_costs(self, lines: list):
        START = self.OFFSET
        END = self.OFFSET + self.nb_depots
        #self.depot_opening_costs = list(map(int, lines[START: END]))
        self.depot_opening_costs = list(map(float, lines[START: END]))

        self.next_offset(self.nb_depots)

    def _transform_dataset(self, lines):
        lines = list(map(lambda line: line.replace('\t', ' '), lines))
        lines = list(map(lambda line: line.replace('\n', ''), lines))
        lines = list(map(lambda line: line.rstrip(), lines))
        lines = list(map(lambda line: line.lstrip(), lines))
        lines = list(filter(lambda line: line != '', lines))

        return lines

    def _load_dataset(self):
        with open(self.path, "r") as f:
            lines = f.readlines()

            lines = self._transform_dataset(lines)

            self.nb_customers = int(lines[self.OFFSET])
            self.next_offset()

            self.nb_depots = int(lines[self.OFFSET])
            self.next_offset()

            self._load_depot_coordinates(lines)

            self._load_customer_coordinates(lines)

            self.vehicle_capacity = float(lines[self.OFFSET])
            self.next_offset()

            self._load_depot_capacities(lines)

            self._load_customer_demands(lines)

            self._load_depot_opening_costs(lines)

            self.route_opening_cost = float(lines[self.OFFSET])
            self.next_offset()

            self.is_int = bool(lines[self.OFFSET] == '1')

    def _find_assignment_costs(self):
        temp_assignment_cost = [[0.0 for x in range(self.nb_customers)] for y in range(self.nb_depots)]

        for i in range(0, self.nb_depots):
            for j in range(0, self.nb_customers):
                ax = self.customer_coordinates_list[j][0]
                ay = self.customer_coordinates_list[j][1]
                bx = self.depot_coordinates_list[i][0]
                by = self.depot_coordinates_list[i][1]
                dist = math.sqrt(math.pow(ax - bx, 2) + math.pow(ay - by, 2))
                if self.is_int == False:
                    dist = dist * 100
                temp_assignment_cost[i][j] = dist

        for i in range(self.nb_customers):
            temp = []
            for j in range(self.nb_depots):
                temp.append(temp_assignment_cost[j][i])
            self.assignment_cost.append(temp)

    def __repr__(self):
        repr = f''
        for key, value in self.__dict__.items():
            repr += f'{key}: {value} \n'
            # print(key, value)

        return repr