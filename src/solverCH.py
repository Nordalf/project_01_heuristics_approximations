import time
import itertools

from data import Data
import solution
import sys

class ConstructionHeuristics:
    total_distance = 0
    def __init__(self,instance):
        self.instance = instance

    def construct(self, time_left):
        return(self.canonical_solution(time_left))

    def canonical_solution(self, time_left):
        sol = solution.Solution(self.instance)
        t0 = time.clock()
        route = [0]
        q=0
        for i in range(1,len(self.instance.nodes)): # we bypass the depot 0            
            if q+self.instance.nodes[i]["rq"] <= self.instance.capacity:
                q+=self.instance.nodes[i]["rq"]
                # Calculate distance between previous and current node added to the route
                # > 0 is to ensure no IndexOutOfBounds Exception
                if len(route) > 0:
                    self.total_distance += round(abs(self.instance.nodes[i-1]["pt"] - self.instance.nodes[i]["pt"]),0)
                route += [i]
            else:
                self.total_distance += round(abs(self.instance.nodes[i-1]["pt"] - self.instance.nodes[i]["pt"]),0)
                sol.routes += [route+[0]]
                route = [0,i]                
                q=self.instance.nodes[i]["rq"]
            if time.clock() - t0 > time_left:
                sys.stdout.write("Time expired")
                return sol
        sol.routes += [route+[0]]
        solution.routes = sol.routes
        return sol