from VRP_Model import *
from SolutionDrawer import *


class Solution:
    def __init__(self):
        self.cost = 0.0
        self.routes = [[]]

    def append(self, sol):
        self.cost += sol.cost
        self.routes.append(sol.routes)

class RelocationMove(object):
    def __init__(self):
        self.originDepotPosition = None
        self.targetDepotPosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.moveCost = None

    def Initialize(self):
        self.originDepotPosition = None
        self.targetDepotPosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.moveCost = 10 ** 9

class SwapMove(object):
    def __init__(self):
        self.positionOfFirstDepot = None
        self.positionOfSecondDepot = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = None

    def Initialize(self):
        self.positionOfFirstDepot = None
        self.positionOfSecondDepot = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = 10 ** 9

class Total_Solver:
    def __init__(self, TotalSolutions, TotalNodes, route_opening_cost, is_int):
        self.cost = TotalSolutions.cost
        self.routes = TotalSolutions.routes
        self.allNodes = TotalNodes
        # self.customers = m.customers
        self.depot = 0
        #self.distanceMatrix = m.matrix
        self.capacity = 0
        self.route_cost = route_opening_cost
        self.is_int = is_int
        self.sol = TotalSolutions
        # self.bestSolution = None

    def solve(self):
        self.LocalSearch(1)
        self.ReportSolution(self.sol)
        self.LocalSearch(0)
        self.ReportSolution(self.sol)
        self.LocalSearch(1)
        self.ReportSolution(self.sol)
        return self.sol

    def LocalSearch(self, operator):
        self.Recalculate_ID()
        self.CreateDistanceMatrix()
        self.bestSolution = self.cloneSolution(self.sol)
        terminationCondition = False
        localSearchIterator = 0

        rm = RelocationMove()
        sm = SwapMove()

        while terminationCondition is False:

            if operator == 0:
                rm.Initialize()
                #SolDrawer.draw(localSearchIterator, self.sol, self.allNodes)
                if len(self.sol.routes) == 1:  # stop condition when only 1 depot
                    rm.originDepotPosition = 1
                # Relocations
                print("Total Relocation Move")
                self.FindBestRelocationMove(rm)
                if rm.originDepotPosition is not None:
                    if rm.moveCost < 0:
                        self.ApplyRelocationMove(rm)
                    else:
                        terminationCondition = True
            elif operator == 1:
                print("Total Swap Move")
                sm.Initialize()
                self.FindBestSwapMove(sm)
                if sm.positionOfFirstRoute is not None:
                    if sm.moveCost < 0:
                        self.ApplySwapMove(sm)
                    else:
                        terminationCondition = True

            self.TestSolution()

            if (self.sol.cost < self.bestSolution.cost):
                self.bestSolution = self.cloneSolution(self.sol)

            localSearchIterator = localSearchIterator + 1
            print("Local Search Iterator: ", localSearchIterator, "Routes solution cost from ls: ", self.sol.cost)

        self.sol = self.bestSolution

    def cloneSolution(self, sol: Solution):
        cloned = Solution()
        cloned.routes = [[] for y in range(len(sol.routes))]
        for i in range(0, len(sol.routes)):
            for j in range(0, len(sol.routes[i])):
                rt = sol.routes[i][j]
                self.depot = self.allNodes[i][0]
                self.capacity = self.routes[i][j].capacity
                clonedRoute = self.cloneRoute(rt)
                cloned.routes[i].append(clonedRoute)
        cloned.cost = self.sol.cost
        return cloned

    def cloneRoute(self, rt: Route):
        cloned = Route(self.depot, self.capacity, self.cost)
        cloned.cost = rt.cost
        cloned.load = rt.load
        cloned.sequenceOfNodes = rt.sequenceOfNodes.copy()
        return cloned

    def FindBestRelocationMove(self, rm):
        for originDepotIndex in range(0, len(self.sol.routes)):
            dp1: Route = self.sol.routes[originDepotIndex]
            for originRoutePosition in range(0, len(dp1)):
                for originNodeIndex in range(1, len(dp1[originRoutePosition].sequenceOfNodes) - 1):
                    for targetDepotIndex in range(0, len(self.sol.routes)):
                        dp2: Route = self.sol.routes[targetDepotIndex]
                        for targetRoutePosition in range(0, len(dp2)):
                            for targetNodeIndex in range(1, len(dp2[targetRoutePosition].sequenceOfNodes) - 1):

                                if originDepotIndex == targetDepotIndex and (
                                        targetNodeIndex == originNodeIndex or targetNodeIndex == originNodeIndex - 1):
                                    continue

                                A = dp1[originRoutePosition].sequenceOfNodes[originNodeIndex - 1]
                                B = dp1[originRoutePosition].sequenceOfNodes[originNodeIndex]
                                C = dp1[originRoutePosition].sequenceOfNodes[originNodeIndex + 1]

                                F = dp2[targetRoutePosition].sequenceOfNodes[targetNodeIndex]
                                G = dp2[targetRoutePosition].sequenceOfNodes[targetNodeIndex + 1]

                                if dp1 != dp2:
                                    if dp2[targetRoutePosition].load + B.demand > dp2[targetRoutePosition].capacity:
                                        continue

                                if dp1 == dp2:
                                    #continue
                                    if originRoutePosition != targetRoutePosition:
                                         if dp2[targetRoutePosition].load + B.demand > dp2[targetRoutePosition].capacity:
                                             continue

                                #self.CreateDistanceMatrix_1(dp1, dp2, i, j)

                                costAdded = self.distanceMatrix[A.ID][C.ID] + self.distanceMatrix[F.ID][B.ID] + \
                                            self.distanceMatrix[B.ID][G.ID]
                                costRemoved = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[B.ID][C.ID] + \
                                              self.distanceMatrix[F.ID][G.ID]

                                originRtCostChange = self.distanceMatrix[A.ID][C.ID] - self.distanceMatrix[A.ID][B.ID] - \
                                                     self.distanceMatrix[B.ID][C.ID]
                                targetRtCostChange = self.distanceMatrix[F.ID][B.ID] + self.distanceMatrix[B.ID][G.ID] - \
                                                     self.distanceMatrix[F.ID][G.ID]

                                moveCost = costAdded - costRemoved
                                #if abs(moveCost) > 0.000001:
                                #    moveCost = 0

                                if (moveCost < rm.moveCost):
                                    self.StoreBestRelocationMove(originDepotIndex, targetDepotIndex, originNodeIndex,
                                                                 targetNodeIndex, moveCost, originRtCostChange,
                                                                 targetRtCostChange, originRoutePosition, targetRoutePosition, rm)

    def CreateDistanceMatrix_1(self, dp1: Route, dp2: Route, i, j):
        self.topic_nodes = []
        for s in range(0, len(dp1[i].sequenceOfNodes) - 1):
            self.topic_nodes.append(dp1[i].sequenceOfNodes[s])
        for s in range(0, len(dp2[j].sequenceOfNodes) - 1):
            self.topic_nodes.append(dp2[j].sequenceOfNodes[s])
        rows = len(self.topic_nodes)
        self.distanceMatrix = [[0.0 for x in range(rows)] for y in range(rows)]

        for k in range(0, len(self.topic_nodes)):
            for l in range(0, len(self.topic_nodes)):
                a = self.topic_nodes[k]
                b = self.topic_nodes[l]
                dist = math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
                self.distanceMatrix[k][l] = dist
        return self.distanceMatrix

    def CreateDistanceMatrix(self):
        rows = 0
        self.topic_nodes = []
        for i in range(0, len(self.allNodes)):
            rows += len(self.allNodes[i])
            for j in range(0, len(self.allNodes[i])):
                self.topic_nodes.append(self.allNodes[i][j])

        self.distanceMatrix = [[0.0 for x in range(rows)] for y in range(rows)]

        for k in range(0, len(self.topic_nodes)):
            for l in range(0, len(self.topic_nodes)):
                a = self.topic_nodes[k]
                b = self.topic_nodes[l]
                dist = math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
                if self.is_int == False:
                    dist = dist * 100
                self.distanceMatrix[k][l] = dist
        return self.distanceMatrix

    def Recalculate_ID(self):
        cntr = 0
        for i in range(0, len(self.allNodes)):
            for j in range(0, len(self.allNodes[i])):
                self.allNodes[i][j].ID = cntr
                cntr += 1

    def StoreBestRelocationMove(self, originDepotIndex, targetDepotIndex, originNodeIndex, targetNodeIndex,
                                moveCost, originRtCostChange, targetRtCostChange, originRoutePosition, targetRoutePosition, rm: RelocationMove):
        rm.originDepotPosition = originDepotIndex
        rm.originNodePosition = originNodeIndex
        rm.targetDepotPosition = targetDepotIndex
        rm.targetNodePosition = targetNodeIndex
        rm.costChangeOriginRt = originRtCostChange
        rm.costChangeTargetRt = targetRtCostChange
        rm.originRoutePosition = originRoutePosition
        rm.targetRoutePosition = targetRoutePosition
        rm.moveCost = moveCost

    def ApplyRelocationMove(self, rm: RelocationMove):

        oldCost = self.CalculateTotalCost(self.sol)

        originRt = self.sol.routes[rm.originDepotPosition]
        targetRt = self.sol.routes[rm.targetDepotPosition]

        B = originRt[rm.originRoutePosition].sequenceOfNodes[rm.originNodePosition]

        if originRt == targetRt:
            if originRt[rm.originRoutePosition] == targetRt[rm.targetRoutePosition]:
                del originRt[rm.originRoutePosition].sequenceOfNodes[rm.originNodePosition]
                if (rm.originNodePosition < rm.targetNodePosition):
                    targetRt[rm.targetRoutePosition].sequenceOfNodes.insert(rm.targetNodePosition, B)
                else:
                    targetRt[rm.targetRoutePosition].sequenceOfNodes.insert(rm.targetNodePosition + 1, B)

                originRt[rm.originRoutePosition].cost += rm.moveCost
            else:
                del originRt[rm.originRoutePosition].sequenceOfNodes[rm.originNodePosition]
                targetRt[rm.targetRoutePosition].sequenceOfNodes.insert(rm.targetNodePosition + 1, B)
                originRt[rm.originRoutePosition].cost += rm.costChangeOriginRt
                targetRt[rm.targetRoutePosition].cost += rm.costChangeTargetRt
                originRt[rm.originRoutePosition].load -= B.demand
                targetRt[rm.targetRoutePosition].load += B.demand
        else:
            del originRt[rm.originRoutePosition].sequenceOfNodes[rm.originNodePosition]
            targetRt[rm.targetRoutePosition].sequenceOfNodes.insert(rm.targetNodePosition + 1, B)
            originRt[rm.originRoutePosition].cost += rm.costChangeOriginRt
            targetRt[rm.targetRoutePosition].cost += rm.costChangeTargetRt
            originRt[rm.originRoutePosition].load -= B.demand
            targetRt[rm.targetRoutePosition].load += B.demand

        self.sol.cost += rm.moveCost

        newCost = self.CalculateTotalCost(self.sol)
        # debuggingOnly
        if abs((newCost - oldCost) - rm.moveCost) > 0.0001:
            print('Cost Issue')

    def CalculateTotalCost(self, sol):
        c = 0
        for i in range(0, len(self.sol.routes)):
            dp = sol.routes[i]
            for k in range(0, len(dp)):
                c += self.route_cost
                for j in range(0, len(dp[k].sequenceOfNodes) - 1):
                    a = dp[k].sequenceOfNodes[j]
                    b = dp[k].sequenceOfNodes[j + 1]
                    c += self.distanceMatrix[a.ID][b.ID]

        return c

    def TestSolution(self):
        totalSolCost = 0
        del_flag = False
        for r in range(0, len(self.sol.routes)):
            rt: Route = self.sol.routes[r]
            for t in range(0, len(rt)):
                if del_flag == True:
                    t -= 1
                if len(rt[t].sequenceOfNodes) <= 2:
                    #self.sol.routes.remove(rt)
                    #self.sol.routes.remove(rt[t].sequenceOfNodes)
                    del self.sol.routes[r][t]
                    del_flag = True
                    self.sol.cost -= self.route_cost
                    continue

                rtCost = self.route_cost
                rtLoad = 0
                for n in range(0, len(rt[t].sequenceOfNodes) - 1):
                    A = rt[t].sequenceOfNodes[n]
                    B = rt[t].sequenceOfNodes[n + 1]
                    rtCost += self.distanceMatrix[A.ID][B.ID]
                    rtLoad += A.demand
                if abs(rtCost - rt[t].cost) > 0.0001:
                    print('Route Cost problem')
                if rtLoad != rt[t].load:
                    print('Route Load problem')

                totalSolCost += rt[t].cost

        if abs(totalSolCost - self.sol.cost) > 0.0001:
            print('Solution Cost problem')

    def ReportSolution(self, sol):
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            print("Depot no", i, ":", end=' \n')
            for t in range(0, len(rt)):
                print("Route no", t, ":", end=' ')
                for j in range(0, len(rt[t].sequenceOfNodes)):
                    if j == len(rt[t].sequenceOfNodes) - 1:
                        print(rt[t].sequenceOfNodes[j].position, end=',')
                    else:
                        print(rt[t].sequenceOfNodes[j].position, end='-')
                print(" Route cost: ", rt[t].cost)
        print("Total routes cost: :", self.sol.cost)

    def FindBestSwapMove(self, sm):
        for firstDepotIndex in range(0, len(self.sol.routes)):
            dp1: Route = self.sol.routes[firstDepotIndex]
            for firstRouteIndex in range(0, len(dp1)):
                for secondDepotIndex in range(firstDepotIndex, len(self.sol.routes)):
                    dp2: Route = self.sol.routes[secondDepotIndex]
                    for secondRouteIndex in range(0, len(dp2)):
                        for firstNodeIndex in range(1, len(dp1[firstRouteIndex].sequenceOfNodes) - 1):
                            # if len(self.sol.routes) == 1 and len(dp1[firstRouteIndex].sequenceOfNodes) <= 3:  # stop condition when only 1 route and less than 4 nodes
                            #     sm.positionOfFirstRoute = 1

                            startOfSecondNodeIndex = 1
                            if dp1 == dp2:
                                startOfSecondNodeIndex = firstNodeIndex + 1
                            for secondNodeIndex in range(startOfSecondNodeIndex, len(dp2[secondRouteIndex].sequenceOfNodes) - 1):

                                a1 = dp1[firstRouteIndex].sequenceOfNodes[firstNodeIndex - 1]
                                b1 = dp1[firstRouteIndex].sequenceOfNodes[firstNodeIndex]
                                c1 = dp1[firstRouteIndex].sequenceOfNodes[firstNodeIndex + 1]

                                a2 = dp2[secondRouteIndex].sequenceOfNodes[secondNodeIndex - 1]
                                b2 = dp2[secondRouteIndex].sequenceOfNodes[secondNodeIndex]
                                c2 = dp2[secondRouteIndex].sequenceOfNodes[secondNodeIndex + 1]

                                moveCost = None
                                costChangeFirstRoute = None
                                costChangeSecondRoute = None

                                if dp1 == dp2:
                                    if dp1[firstRouteIndex] == dp2[secondRouteIndex]:
                                        if firstNodeIndex == secondNodeIndex - 1:
                                            costRemoved = self.distanceMatrix[a1.ID][b1.ID] + self.distanceMatrix[b1.ID][b2.ID] + \
                                                          self.distanceMatrix[b2.ID][c2.ID]
                                            costAdded = self.distanceMatrix[a1.ID][b2.ID] + self.distanceMatrix[b2.ID][b1.ID] + \
                                                        self.distanceMatrix[b1.ID][c2.ID]
                                            moveCost = costAdded - costRemoved
                                        else:

                                            costRemoved1 = self.distanceMatrix[a1.ID][b1.ID] + self.distanceMatrix[b1.ID][c1.ID]
                                            costAdded1 = self.distanceMatrix[a1.ID][b2.ID] + self.distanceMatrix[b2.ID][c1.ID]
                                            costRemoved2 = self.distanceMatrix[a2.ID][b2.ID] + self.distanceMatrix[b2.ID][c2.ID]
                                            costAdded2 = self.distanceMatrix[a2.ID][b1.ID] + self.distanceMatrix[b1.ID][c2.ID]
                                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                                    else:
                                        if dp1[firstRouteIndex].load - b1.demand + b2.demand > self.capacity:
                                            continue
                                        if dp2[secondRouteIndex].load - b2.demand + b1.demand > self.capacity:
                                            continue

                                        costRemoved1 = self.distanceMatrix[a1.ID][b1.ID] + self.distanceMatrix[b1.ID][c1.ID]
                                        costAdded1 = self.distanceMatrix[a1.ID][b2.ID] + self.distanceMatrix[b2.ID][c1.ID]
                                        costRemoved2 = self.distanceMatrix[a2.ID][b2.ID] + self.distanceMatrix[b2.ID][c2.ID]
                                        costAdded2 = self.distanceMatrix[a2.ID][b1.ID] + self.distanceMatrix[b1.ID][c2.ID]

                                        costChangeFirstRoute = costAdded1 - costRemoved1
                                        costChangeSecondRoute = costAdded2 - costRemoved2

                                        moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                                else:
                                    if dp1[firstRouteIndex].load - b1.demand + b2.demand > self.capacity:
                                        continue
                                    if dp2[secondRouteIndex].load - b2.demand + b1.demand > self.capacity:
                                        continue

                                    costRemoved1 = self.distanceMatrix[a1.ID][b1.ID] + self.distanceMatrix[b1.ID][c1.ID]
                                    costAdded1 = self.distanceMatrix[a1.ID][b2.ID] + self.distanceMatrix[b2.ID][c1.ID]
                                    costRemoved2 = self.distanceMatrix[a2.ID][b2.ID] + self.distanceMatrix[b2.ID][c2.ID]
                                    costAdded2 = self.distanceMatrix[a2.ID][b1.ID] + self.distanceMatrix[b1.ID][c2.ID]

                                    costChangeFirstRoute = costAdded1 - costRemoved1
                                    costChangeSecondRoute = costAdded2 - costRemoved2

                                    moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)
                                    #if abs(moveCost) > 0.000001:
                                    #    moveCost = 0

                                if moveCost < sm.moveCost:
                                    self.StoreBestSwapMove(firstDepotIndex, secondDepotIndex, firstNodeIndex, secondNodeIndex,
                                                           firstRouteIndex, secondRouteIndex,
                                                           moveCost, costChangeFirstRoute, costChangeSecondRoute, sm)

    def StoreBestSwapMove(self, firstDepotIndex, secondDepotIndex, firstNodeIndex, secondNodeIndex, firstRouteIndex,
                          secondRouteIndex, moveCost, costChangeFirstRoute, costChangeSecondRoute, sm):
        sm.positionOfFirstDepot = firstDepotIndex
        sm.positionOfSecondDepot = secondDepotIndex
        sm.positionOfFirstNode = firstNodeIndex
        sm.positionOfSecondNode = secondNodeIndex
        sm.costChangeFirstRt = costChangeFirstRoute
        sm.costChangeSecondRt = costChangeSecondRoute
        sm.positionOfFirstRoute = firstRouteIndex
        sm.positionOfSecondRoute = secondRouteIndex
        sm.moveCost = moveCost

    def ApplySwapMove(self, sm):
        oldCost = self.CalculateTotalCost(self.sol)
        rt1 = self.sol.routes[sm.positionOfFirstDepot]
        rt2 = self.sol.routes[sm.positionOfSecondDepot]
        b1 = rt1[sm.positionOfFirstRoute].sequenceOfNodes[sm.positionOfFirstNode]
        b2 = rt2[sm.positionOfSecondRoute].sequenceOfNodes[sm.positionOfSecondNode]
        rt1[sm.positionOfFirstRoute].sequenceOfNodes[sm.positionOfFirstNode] = b2
        rt2[sm.positionOfSecondRoute].sequenceOfNodes[sm.positionOfSecondNode] = b1

        if (rt1 == rt2):
            if rt1[sm.positionOfFirstRoute] == rt2[sm.positionOfSecondRoute]:
                rt1[sm.positionOfFirstRoute].cost += sm.moveCost
            else:
                rt1[sm.positionOfFirstRoute].cost += sm.costChangeFirstRt
                rt2[sm.positionOfSecondRoute].cost += sm.costChangeSecondRt
                rt1[sm.positionOfFirstRoute].load = rt1[sm.positionOfFirstRoute].load - b1.demand + b2.demand
                rt2[sm.positionOfSecondRoute].load = rt2[sm.positionOfSecondRoute].load + b1.demand - b2.demand
        else:
            rt1[sm.positionOfFirstRoute].cost += sm.costChangeFirstRt
            rt2[sm.positionOfSecondRoute].cost += sm.costChangeSecondRt
            rt1[sm.positionOfFirstRoute].load = rt1[sm.positionOfFirstRoute].load - b1.demand + b2.demand
            rt2[sm.positionOfSecondRoute].load = rt2[sm.positionOfSecondRoute].load + b1.demand - b2.demand

        self.sol.cost += sm.moveCost

        newCost = self.CalculateTotalCost(self.sol)
        # debuggingOnly
        if abs((newCost - oldCost) - sm.moveCost) > 0.0001:
            print('Cost Issue')
