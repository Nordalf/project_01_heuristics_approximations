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
        return(self.clusterAlgorithm(time_left))

    def euclideanDistance(self, coordinate1, coordinate2):
        return pow(pow(coordinate1.x - coordinate2.x, 2) + pow(coordinate1.y - coordinate2.y, 2), .5)

    def clusterAlgorithm(self, time_left):
        # To implement
        "This heuristic algorithm makes a several clusters of points, where each cluster is <= maxCapacity. When clusters"
        " have been found for all points, then we send a vehicle out to each cluster and find the routes."
        "1 ) Pick a (random) point"
        "2 ) Calculate the euclidean distance to all points to find a cluster, which does not exceed maximum capacity"
        "3 ) Send a vehicle to the cluster and find the shortest route in the cluster"
        "4 ) Repeat"
        "Hvordan håndterer vi kunder, som ikke er i clusters?"
        sol = solution.Solution(self.instance)
        t0 = time.clock()
        route = [0]
        q=0
        visited = []
        clusters = []
        for i in range(len(self.instance.nodes)-1):
            for j in range(1,len(self.instance.nodes)):
                temp = self.euclideanDistance(self.instance.nodes[current]["pt"], self.instance.nodes[j]["pt"])
                if j not in visited:                    
                    if temp <= shortestDistance:
                        shortestDistance = temp
                        current = j
                        visited += [j]
                        if q+self.instance.nodes[current]["rq"] <= self.instance.capacity:
                            q+=self.instance.nodes[current]["rq"]                            
                            if len(route) > 0:
                                self.total_distance += shortestDistance
                            route += [current]                            
                        else:
                            self.total_distance += shortestDistance
                            sol.routes += [route+[0]]
                            route = [0,current]                
                            q=self.instance.nodes[current]["rq"]
            shortestDistance = 10000000
            if time.clock() - t0 > time_left:
                sys.stdout.write("Time expired")
                return sol

        sol.routes += [route+[0]]
        solution.routes = sol.routes
        return sol
