# Ant Colony Optimization applied on the Capacitated Vehicle Routing Problem
# We are using ants to simulate vehicles and its complete set of routes 
# is constructed by successively choosing customers to visit 
# until all the customers have been visited.
#
# A new route is started, when the constraint on the capacity has been breached. 
# each ant is assigned to a randomly chosen
# customer as its first city to visit from the depot. Then, at
# each construction step, an ant k at current city i will
# select the next city j to visit from a feasible neighborhood
# Variables needed:
#   - distance - d(i,j)
#   - heuristic value (eta) - 1/d(i,j) - the attractiveness
#   - pheromone concentration on the edges - t = tau(i, j)
#   - savings of combining two cities - m = mu(i,j)=d(i,0) + d(j,0) - d(i,j)

# TODO
# Create a map of pheromone between two points
# Append pheromone on a trail already visited
# Decay pheromone at every iteration. Decay with small amounts 

# 23/05/2019 - NOT WORKING. 

import random
import numpy as np


def euclideanDistance(coordinate1, coordinate2):
    return pow(pow(coordinate1.x - coordinate2.x, 2) + pow(coordinate1.y - coordinate2.y, 2), .5)

class Ant:
    """
        Ants build solutions probabilistically without updating pheromone trails
    """
    c = 1.0 # Original number of trails
    alpha = 1 # controls pheromone importance
    beta = 5 # controls the distance priority - should be greater than alpha
    evaporation = 0.05 # percentage of how much pheromone is evaporated / decayed pr iteration
    ant_factor = 0.8 # the amount of ants used pr request

    no_of_ants = 5 # The number of ants needed to try and find a solution
    max_iterations = 1000 # The maximum number of iterations one ant is going to try

    pheromone_map = {} # A dictionary of the pheromone level from one request to another
    probability_of_going_to_request = {} # The Pheromone Map

    global_best = 0
    global_best_route = []

    def aco(self, data, solution, output_file=None):
        route = [0]
        Q = data.capacity # Max Capacity
        q = 0 # Collected capacity
        distance = 0
        not_visited_nodes = {}
        
        local_best = 0
        local_best_route = []
        
        sum_of_all_available_requests_score = 0

        # Start by initializing all the pheromone level for every possible trail
        for first_entry in range(len(data.nodes)):
            self.pheromone_map[data.nodes[first_entry]['id']] = {}
            for second_entry in range(len(data.nodes)):
                if first_entry != second_entry:
                    distance = euclideanDistance(data.nodes[first_entry]['pt'], data.nodes[second_entry]['pt']) # Calculate the distance
                    init_pheromone = 1 / distance
                    self.pheromone_map[data.nodes[first_entry]['id']][data.nodes[second_entry]['id']] = {"pheromone": init_pheromone, "distance" : distance }
                    sum_of_all_available_requests_score += self.pheromone_map[data.nodes[first_entry]['id']][data.nodes[second_entry]['id']]["pheromone"] # Summation of all scores
        
            
        counter = 0
        while True:
            
            # Creating a map of unvisited nodes
            for i in range(1, len(data.nodes)):
                not_visited_nodes[data.nodes[i]["id"]-1] = {
                        "id": data.nodes[i]["id"],
                        "rq": data.nodes[i]["rq"],
                    }

            # Pick a random point to start off with            
            current_request = random.choice(list(not_visited_nodes)) # The first choice is random chosen
            # print("First Random Pick: ", current_request)
            q += data.nodes[current_request]["rq"] # Update the current capacity used for the route
            route += [current_request] # Add it to the route

            del not_visited_nodes[current_request] # Remove the randomly picked, since it has been "marked" as visited now
            
            previous_score = 0
            picked_request = 0
            
            while len(not_visited_nodes) != 0:
                
                for key, value in self.pheromone_map[current_request].items():
                    if len(not_visited_nodes) == 1:
                        if key in not_visited_nodes.keys():
                            picked_request = key
                            break
                    # print(self.pheromone_map[current_request][key]["distance"])
                    request_to_request_score = self.pheromone_map[current_request][key]["pheromone"] ** self.alpha * ((1.0 / self.pheromone_map[current_request][key]["distance"]) ** self.beta) # Calculate the probabiltity
                    prob_go_to_request = request_to_request_score / sum_of_all_available_requests_score
                    if previous_score == 0: # one time
                        if key in not_visited_nodes.keys():
                            previous_score = prob_go_to_request
                            picked_request = key
                    if prob_go_to_request > previous_score: # If the probability is higher, choose this point
                        if key in not_visited_nodes.keys():
                            picked_request = key # The highest probability request is chosen                           

                    previous_score = prob_go_to_request
                
                # Since we have found the next address to visit, we can append the pheromone level
                # print("Current: ", current_request, " - Picked: ", picked_request, " - Len NV: ", len(not_visited_nodes))
                
                selected_next_address_distance = euclideanDistance(data.nodes[current_request-1]['pt'], data.nodes[picked_request-1]['pt'])
                self.pheromone_map[current_request][picked_request]["pheromone"] += 1 / selected_next_address_distance

                if q+data.nodes[picked_request]['rq'] <= Q: # Check capacity constraint
                    q += data.nodes[picked_request]["rq"] # Update the current capacity used for the route
                    del not_visited_nodes[picked_request] # Remove request from the list
                    if len(not_visited_nodes) == 0: # Since the while loop is going to end after this, we are adding the route to all the routes
                        route += [picked_request]
                        local_best_route += [route+[0]]
                        route = [0]
                    current_request = picked_request # New current request
                    route += [current_request]
                    previous_score = 0
                else:
                    current_request = picked_request # Starting point for next
                    local_best_route += [route+[0]]
                    route = [0]
                    route += [current_request]
                    del not_visited_nodes[current_request] # Remove request from the list
                    q = data.nodes[current_request]["rq"]
                    previous_score = 0

            solution.routes = local_best_route
            cost = solution.cost()
            
            if local_best == 0:
                local_best = cost
                self.global_best = cost
            if cost < local_best:
                local_best = cost
                # local_best_route = solution.routes
                print("New Local Best Route")
                if local_best < self.global_best:
                    self.global_best = local_best
                    self.global_best_route = local_best_route
                    solution.routes = self.global_best_route
                    print("New Global Best Route", solution.cost())
                    if output_file is not None:
                        assert solution.valid_solution()
                        print("Hre")
                        solution.write_to_file(output_file+'.sol')
            # Reset the route
            route = []
            # Reset the solution routes
            local_best_route = []
            # Evaporate by .05 % for every pheromone trail
            for i in range(1, len(self.pheromone_map)):
                for j in range(1, len(self.pheromone_map[i])):
                    if i != j:
                        self.pheromone_map[i][j]["pheromone"] = self.pheromone_map[i][j]["pheromone"] * (1 - self.evaporation)
            q = 0
            counter += 1
                # print("Pheromone Map: ", self.pheromone_map)
        print(self.global_best_route)
        solution.routes = self.global_best_route
        return solution
        
        
    def algorithm(self, data, solution, seed=None, output_file=None):
        random.seed(seed)
        solution = self.aco(data, solution, output_file=output_file)
        # local_best = solution.cost()
        
        print("Cost", self.global_best)
        return solution



