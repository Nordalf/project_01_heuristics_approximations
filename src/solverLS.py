import time
import itertools

import data
import solution
import sys

class SolverLS:
    # total_distance = 0
    solution = None
    calculated_route_capacity = []
    def __init__(self,solution):
        self.solution = solution

    def euclideanDistance(self, coordinate1, coordinate2):
        return pow(pow(coordinate1.x - coordinate2.x, 2) + pow(coordinate1.y - coordinate2.y, 2), .5)

    # Kind of "dirty" code to get the job done
    def calculate_routes_capacities(self):
        result = 0
        del self.calculated_route_capacity[:]
        print(len(self.solution.routes))
        for i in range(len(self.solution.routes)):
            for j in range(len(self.solution.routes[i])):
                result += self.solution.routes[i][j]
            self.calculated_route_capacity += [result]
            result = 0

    # First attempt - Compare two routes
    # Husk at beregne til det næste punkt, som der bliver byttet ud med
    def close_index_route_swap(self):
        "self.solution = 2D-array solution/routes"
        # t0 = time.clock()
        counter = 0
        exit_criteria = True
        self.calculate_routes_capacities()
        # print("SOLUTION: ", self.calculated_route_capacity)
        for i in range(len(self.solution.routes)-1):
            for j in range(len(self.solution.routes[i])):
                try:
                    # Triangle Inequality                    
                    sidea_dist_r1 = self.euclideanDistance(self.solution.instance.nodes[self.solution.routes[i][j]]["pt"], self.solution.instance.nodes[self.solution.routes[i][j+1]]["pt"])
                    sideb_dist_r1 = self.euclideanDistance(self.solution.instance.nodes[self.solution.routes[i][j+1]]["pt"], self.solution.instance.nodes[self.solution.routes[i+1][j+1]]["pt"])
                    sidec_dist_r1 = self.euclideanDistance(self.solution.instance.nodes[self.solution.routes[i][j]]["pt"], self.solution.instance.nodes[self.solution.routes[i+1][j+1]]["pt"])
                    # sidea_dist_r2 = self.euclideanDistance(self.solution.instance.nodes[self.solution.routes[i+1][j]]["pt"], self.solution.instance.nodes[self.solution.routes[i+1][j+1]]["pt"])
                    # sidec_dist_r2 = self.euclideanDistance(self.solution.instance.nodes[self.solution.routes[i+1][j]]["pt"], self.solution.instance.nodes[self.solution.routes[i][j+1]]["pt"])
                    if sidea_dist_r1 + sideb_dist_r1 > sidec_dist_r1: #Triangle Inequality by contradiction withhold
                        if sidec_dist_r1 < sidea_dist_r1: # We can make a swap                            
                            if (self.calculated_route_capacity[i] - self.solution.instance.nodes[self.solution.routes[i][j+1]]["rq"] + self.solution.instance.nodes[self.solution.routes[i+1][j+1]]["rq"]) <= self.solution.instance.capacity:
                                tempPointer = self.solution.routes[i+1][j+1]
                                self.solution.routes[i+1][j+1] = self.solution.routes[i][j+1]
                                self.solution.routes[i][j+1] = tempPointer
                                # current_total_distance = current_total_distance - sidea_dist_r1 + sidec_dist_r1 - sidea_dist_r2 + sidec_dist_r2
                            else:
                                pass     
                except IndexError:
                    pass
                    
                    
                    # if time.clock() - t0 > time_left:
                    #     sys.stdout.write("Time expired")
                    #     return self.solution

        # self.total_distance = current_total_distance
        # return self.solution


    # First loop:
    #   Index to keep track of the single route you are processing
    # Second loop:
    #   Index for each element in first route being compared
    # Third loop:
    #   Index for each element in the second route being compared
    def all_combination_route_swap(self):
        "self.solution = 2D-array solution/routes"
        # t0 = time.clock()
        for i in range(len(self.solution.routes)-1):
            if i+1 < len(self.solution.routes):
                for j in range(len(self.solution.routes[i])-1):
                    for k in range(len(self.solution.routes[i+1])-1):
                        try:
                            sidea_r1 = self.euclideanDistance(self.solution.instance.nodes[self.solution.routes[i][k]]["pt"], self.solution.instance.nodes[self.solution.routes[i][k+1]]["pt"])
                            sidec_r1 = self.euclideanDistance(self.solution.instance.nodes[self.solution.routes[i][k]]["pt"], self.solution.instance.nodes[self.solution.routes[i+1][k+1]]["pt"])
                            
                            # Route two to equalize the swap in route one 
                            sidea_r2 = self.euclideanDistance(self.solution.instance.nodes[self.solution.routes[i+1][k]]["pt"], self.solution.instance.nodes[self.solution.routes[i+1][k+1]]["pt"])
                            # Side B Route 2 is the same as Side B Route 1
                            sidec_r2 = self.euclideanDistance(self.solution.instance.nodes[self.solution.routes[i+1][k]]["pt"], self.solution.instance.nodes[self.solution.routes[i+1][k+1]]["pt"])

                            if sidea_r1 > sidec_r1:
                                # Keeping the MAX capacity
                                if (self.calculated_route_capacity[i] - self.solution.instance.nodes[self.solution.routes[i][k+1]]["rq"] + self.solution.instance.nodes[self.solution.routes[i+1][k+1]]["rq"]) <= self.solution.instance.capacity:
                                    if (self.calculated_route_capacity[i] - self.solution.instance.nodes[self.solution.routes[i+1][k+1]]["rq"] + self.solution.instance.nodes[self.solution.routes[i][k+1]]["rq"]) <= self.solution.instance.capacity:
                                        if self.solution.routes[i+1][k+1] != 0 and self.solution.routes[i][k+1] != 0:
                                            tempPointer = self.solution.routes[i+1][k+1]
                                            self.solution.routes[i+1][k+1] = self.solution.routes[i][k+1]
                                            self.solution.routes[i][k+1] = tempPointer
                                            # current_total_distance = current_total_distance - sidea_r1 + sidec_r1 - sidea_r2 + sidec_r2
                        except IndexError:
                            continue
                    
            # if time.clock() - t0 > time_left:
            #     sys.stdout.write("Time expired")
            #     return self.solution

        # self.total_distance = current_total_distance
        # return self.solution

    def run_first(self):
        self.close_index_route_swap()
        return self.solution

    def run_second(self):
        self.all_combination_route_swap()
        return self.solution