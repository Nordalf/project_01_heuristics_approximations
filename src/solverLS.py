import time
import itertools

import data
import solution
import sys

class LocalSearch:
    total_distance = 0
    def __init__(self,instance):
        self.instance = instance

    def euclideanDistance(self, coordinate1, coordinate2):
        return pow(pow(coordinate1.x - coordinate2.x, 2) + pow(coordinate1.y - coordinate2.y, 2), .5)

    def local_search(self, start_sol, time_left):
        # To implement
        t0 = time.clock()
        route = [0]
        q=0
        shortestDistance = 0
        markedPoints = {}
        idx = 0
        for i in range(len(self.instance.nodes)-1): # we bypass the depot 0
            print(route)
            markedPoints[i] = True
            for j in range(1, len(self.instance.nodes)):
                if q+self.instance.nodes[i]["rq"] <= self.instance.capacity:
                    q+=self.instance.nodes[i]["rq"]
                    # We do not need to find the distance for the same point
                    if self.instance.nodes[i]["pt"] != self.instance.nodes[j]["pt"]:
                        if j == 1:
                            shortestDistance = self.euclideanDistance(self.instance.nodes[j]["pt"], self.instance.nodes[i]["pt"])
                        tempDist = self.euclideanDistance(self.instance.nodes[j]["pt"], self.instance.nodes[i]["pt"])
                        if tempDist < shortestDistance:
                            shortestDistance = tempDist
                            
                            route += [j]
                            self.total_distance += round(abs(self.instance.nodes[i-1]["pt"] - self.instance.nodes[i]["pt"]),0)
                else:
                    self.total_distance += round(abs(self.instance.nodes[i-1]["pt"] - self.instance.nodes[i]["pt"]),0)
                    start_sol.routes += [route+[0]]
                    route = [0,j]
                    q=self.instance.nodes[i]["rq"]
            if time.clock() - t0 > time_left:
                sys.stdout.write("Time expired")
                return start_sol
        start_sol.routes += [route+[0]]
        solution.routes = start_sol.routes
        return start_sol
