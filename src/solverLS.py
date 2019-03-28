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

    # First attempt - Compare two routes
    # Husk at beregne til det næste punkt, som der bliver byttet ud med
    def local_search2(self, start_sol, current_total_distance, time_left):
        "start_sol = 2D-array solution/routes"
        t0 = time.clock()
        #print("BEFORE: ", start_sol.routes)
        counter = 0
        exit_criteria = True
        while exit_criteria:
            for i in range(len(start_sol.routes)-1):
                for j in range(len(start_sol.routes[i])):
                    try:
                        # Triangle Inequality                    
                        sidea_dist_r1 = self.euclideanDistance(self.instance.nodes[start_sol.routes[i][j]]["pt"], self.instance.nodes[start_sol.routes[i][j+1]]["pt"])
                        sideb_dist_r1 = self.euclideanDistance(self.instance.nodes[start_sol.routes[i][j+1]]["pt"], self.instance.nodes[start_sol.routes[i+1][j+1]]["pt"])
                        sidec_dist_r1 = self.euclideanDistance(self.instance.nodes[start_sol.routes[i][j]]["pt"], self.instance.nodes[start_sol.routes[i+1][j+1]]["pt"])
                        sidea_dist_r2 = self.euclideanDistance(self.instance.nodes[start_sol.routes[i+1][j]]["pt"], self.instance.nodes[start_sol.routes[i+1][j+1]]["pt"])
                        sidec_dist_r2 = self.euclideanDistance(self.instance.nodes[start_sol.routes[i+1][j]]["pt"], self.instance.nodes[start_sol.routes[i][j+1]]["pt"])
                        if sidea_dist_r1 + sideb_dist_r1 > sidec_dist_r1: #Triangle Inequality by contradiction withhold
                            if sidec_dist_r1 < sidea_dist_r1: # We can make a swap                            
                                if (start_sol.route_rq_slack[i] - self.instance.nodes[start_sol.routes[i][j+1]]["rq"] + self.instance.nodes[start_sol.routes[i+1][j+1]]["rq"]) <= self.instance.capacity:
                                    tempPointer = start_sol.routes[i+1][j+1]
                                    start_sol.routes[i+1][j+1] = start_sol.routes[i][j+1]
                                    start_sol.routes[i][j+1] = tempPointer
                                    current_total_distance = current_total_distance - sidea_dist_r1 + sidec_dist_r1 - sidea_dist_r2 + sidec_dist_r2
                                else:
                                    counter += 1
                                    if counter == 5:
                                        exit_criteria = False
                                    pass
                                    #print("Not enough capacity")
                    except IndexError:
                        pass
                            #print('Out of Range')
                    
                    if time.clock() - t0 > time_left:
                        sys.stdout.write("Time expired")
                        return start_sol

        #print("AFTER: ", start_sol.routes)
        self.total_distance = current_total_distance
        return start_sol


    #Første loop:
    #   Index for at holde styr på den enkelte rute, som man er igang med

    #Andet loop:
    #   Index til hvert element i første rute

    #Tredje loop:
	#   Index til hvert element i anden rute
    # Husk at beregne til det næste punkt, som der bliver byttet ud med
    def local_search3(self, start_sol, current_total_distance, time_left):
        "start_sol = 2D-array solution/routes"
        t0 = time.clock()
        #print("BEFORE: ", start_sol.routes)
        exit_criteria = True
        #while exit_criteria:
        for i in range(len(start_sol.routes)-1):
            if i+1 < len(start_sol.routes):
                for j in range(len(start_sol.routes[i])-1):
                    for k in range(len(start_sol.routes[i+1])-1):
                        try:
                            sidea_r1 = self.euclideanDistance(self.instance.nodes[start_sol.routes[i][k]]["pt"], self.instance.nodes[start_sol.routes[i][k+1]]["pt"])
                            #sideb_r1 = self.euclideanDistance(self.instance.nodes[start_sol.routes[i][k+1]]["pt"], self.instance.nodes[start_sol.routes[i+1][k+1]]["pt"])
                            sidec_r1 = self.euclideanDistance(self.instance.nodes[start_sol.routes[i][k]]["pt"], self.instance.nodes[start_sol.routes[i+1][k+1]]["pt"])
                            
                            # Route two to equalize the swap in route one 
                            sidea_r2 = self.euclideanDistance(self.instance.nodes[start_sol.routes[i+1][k]]["pt"], self.instance.nodes[start_sol.routes[i+1][k+1]]["pt"])
                            # Side B Route 2 is the same as Side B Route 1
                            sidec_r2 = self.euclideanDistance(self.instance.nodes[start_sol.routes[i+1][k]]["pt"], self.instance.nodes[start_sol.routes[i+1][k+1]]["pt"])

                            if sidea_r1 > sidec_r1:
                                # Keeping the MAX capacity
                                if (start_sol.route_rq_slack[i] - self.instance.nodes[start_sol.routes[i][k+1]]["rq"] + self.instance.nodes[start_sol.routes[i+1][k+1]]["rq"]) <= self.instance.capacity:
                                    if (start_sol.route_rq_slack[i+1] - self.instance.nodes[start_sol.routes[i+1][k+1]]["rq"] + self.instance.nodes[start_sol.routes[i][k+1]]["rq"]) <= self.instance.capacity:
                                        if start_sol.routes[i+1][k+1] != 0 and start_sol.routes[i][k+1] != 0:
                                            tempPointer = start_sol.routes[i+1][k+1]
                                            start_sol.routes[i+1][k+1] = start_sol.routes[i][k+1]
                                            start_sol.routes[i][k+1] = tempPointer
                                            current_total_distance = current_total_distance - sidea_r1 + sidec_r1 - sidea_r2 + sidec_r2
                        except IndexError:
                            continue
                    
            if time.clock() - t0 > time_left:
                sys.stdout.write("Time expired")
                return start_sol

        #print("AFTER: ", start_sol.routes)
        self.total_distance = current_total_distance
        return start_sol
