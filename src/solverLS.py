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
        "start_sol = 2D-array solution/routes"
        # To implement
        t0 = time.clock()
        route = [0]
        q=0
        swap = False
        distance_route1 = 0
        distance_route2 = 0
        for i in range(len(start_sol)):
            for j in range(1, len(start_sol)):
                temp = self.euclideanDistance(self.instance.nodes[current]["pt"], self.instance.nodes[j]["pt"])
                start_sol[i][j] = 

        return start_sol

    def swap(self, route1_element, route2_element):
        temp = route1_element
        route1_element = route2_element
        route2_element = temp
        del temp
        return (route1_element, route2_element)
