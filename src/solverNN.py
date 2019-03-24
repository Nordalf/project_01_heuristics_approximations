import time
import itertools

import data
import solution
import sys

class NearestNeighbour:
    total_distance = 0
    def __init__(self,instance):
        self.instance = instance

    def construct(self, time_left):
        return(self.algorithm(time_left))

    def euclideanDistance(self, coordinate1, coordinate2):
        return pow(pow(coordinate1.x - coordinate2.x, 2) + pow(coordinate1.y - coordinate2.y, 2), .5)

    def algorithm(self, time_left):
        # To implement
        "This heuristic algorithm runs through the destinations like a two dimensional array"
        "The first loop is more a less to ensure every node is visited"
        "The second loop starts at node 0 and finds its nearest neightbor. The nearest neightbor is then set to the current node"
        "to continue the path from that node. This continues until no more capacity is available in the truck."
        "This continues until all nodes have been visited."
        sol = solution.Solution(self.instance)
        t0 = time.clock()
        route = [0]
        q=0
        # Until further notice
        shortestDistance = 100000
        route_total_distance = 0
        current = 0
        visited = []
        
        for i in range(len(self.instance.nodes)-1):
            for j in range(1,len(self.instance.nodes)):
                temp = self.euclideanDistance(self.instance.nodes[current]["pt"], self.instance.nodes[j]["pt"])
                if j not in visited:                    
                    if temp < shortestDistance:
                        shortestDistance = temp
                        current = j
                        visited += [j]
                        if q+self.instance.nodes[current]["rq"] <= self.instance.capacity:
                            q+=self.instance.nodes[current]["rq"]
                            if len(route) > 0:
                                self.total_distance += shortestDistance
                                route_total_distance += shortestDistance
                            route += [current]
                        else:
                            sol.route_distances += [route_total_distance]
                            route_total_distance = 0
                            sol.route_rq_slack += [q]
                            sol.routes += [route+[0]]
                            route = [0,current]
                            q=self.instance.nodes[current]["rq"]
            shortestDistance = 10000000
            if time.clock() - t0 > time_left:
                sys.stdout.write("Time expired")
                return sol
        sol.route_distances += [route_total_distance]
        sol.route_rq_slack += [q]
        sol.routes += [route+[0]]
        solution.routes = route
        solution.route_distances = sol.route_distances
        return sol
